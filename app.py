"""A beginner-friendly Flask REST API for managing courses."""

import json
import os
import tempfile
import threading
from datetime import date, datetime, timezone
from pathlib import Path

from flask import Flask, jsonify, request


app = Flask(__name__)

# Keep the JSON file beside this Python file, regardless of the current
# directory from which the application is started.
COURSES_FILE = Path(__file__).resolve().parent / "courses.json"

VALID_STATUSES = {"Not Started", "In Progress", "Completed"}
REQUIRED_FIELDS = ("name", "description", "target_date", "status")

# This lock prevents two requests in this Flask process from changing the file
# at exactly the same time.
file_lock = threading.Lock()


class CourseFileError(Exception):
    """Raised when the courses file cannot be read or written."""


def ensure_courses_file():
    """Create an empty courses.json file when it does not already exist."""
    if not COURSES_FILE.exists():
        save_courses([])


def load_courses():
    """Read and return all courses stored in the JSON file."""
    try:
        ensure_courses_file()
        with COURSES_FILE.open("r", encoding="utf-8") as file:
            courses = json.load(file)

        # The API expects the top-level JSON value to always be a list.
        if not isinstance(courses, list):
            raise CourseFileError("courses.json must contain a JSON list.")

        return courses
    except CourseFileError:
        raise
    except (OSError, json.JSONDecodeError) as error:
        raise CourseFileError(f"Could not read courses.json: {error}") from error


def save_courses(courses):
    """Safely write the complete course list to courses.json."""
    temporary_path = None

    try:
        # Write to a temporary file first. Replacing the real file afterward
        # helps prevent partially written JSON if writing is interrupted.
        with tempfile.NamedTemporaryFile(
            mode="w",
            encoding="utf-8",
            dir=COURSES_FILE.parent,
            delete=False,
        ) as temporary_file:
            json.dump(courses, temporary_file, indent=2, ensure_ascii=False)
            temporary_file.write("\n")
            temporary_path = temporary_file.name

        os.replace(temporary_path, COURSES_FILE)
    except (OSError, TypeError) as error:
        # Clean up a leftover temporary file when possible.
        if temporary_path:
            try:
                Path(temporary_path).unlink(missing_ok=True)
            except OSError:
                pass
        raise CourseFileError(f"Could not write courses.json: {error}") from error


def validate_course_data(data):
    """Return a validation error message, or None when the data is valid."""
    if not isinstance(data, dict):
        return "Request body must be a JSON object."

    missing_fields = [
        field
        for field in REQUIRED_FIELDS
        if field not in data
        or data[field] is None
        or (isinstance(data[field], str) and not data[field].strip())
    ]
    if missing_fields:
        return f"Missing required fields: {', '.join(missing_fields)}."

    if data["status"] not in VALID_STATUSES:
        allowed = ", ".join(sorted(VALID_STATUSES))
        return f"Invalid status. Status must be one of: {allowed}."

    try:
        # fromisoformat checks that the value is a real date such as 2026-10-21.
        date.fromisoformat(data["target_date"])
    except (TypeError, ValueError):
        return "Invalid target_date. Use the YYYY-MM-DD format."

    return None


def find_course(courses, course_id):
    """Find one course by ID, returning None when it does not exist."""
    return next(
        (course for course in courses if course.get("id") == course_id),
        None,
    )


@app.errorhandler(CourseFileError)
def handle_course_file_error(error):
    """Convert file errors into a useful JSON response."""
    app.logger.error("%s", error)
    return jsonify({"error": str(error)}), 500


# Create courses.json when the module is loaded, including when Flask starts
# the application with the `flask --app app run` command.
try:
    ensure_courses_file()
except CourseFileError as error:
    # Keep the API available so later requests can return a JSON file error.
    app.logger.error("%s", error)


@app.route("/api/courses", methods=["POST"])
def create_course():
    """Add a new course."""
    data = request.get_json(silent=True)
    error = validate_course_data(data)
    if error:
        return jsonify({"error": error}), 400

    with file_lock:
        courses = load_courses()

        # max(..., default=0) makes the first generated ID equal to 1.
        next_id = max(
            (course.get("id", 0) for course in courses),
            default=0,
        ) + 1

        course = {
            "id": next_id,
            "name": data["name"].strip(),
            "description": data["description"].strip(),
            "target_date": data["target_date"],
            "status": data["status"],
            "created_at": datetime.now(timezone.utc).isoformat(),
        }
        courses.append(course)
        save_courses(courses)

    return jsonify(course), 201


@app.route("/api/courses", methods=["GET"])
def get_courses():
    """Return all courses."""
    with file_lock:
        courses = load_courses()
    return jsonify(courses), 200


@app.route("/api/courses/stats", methods=["GET"])
def get_course_stats():
    """Return the total number of courses and totals grouped by status."""
    with file_lock:
        courses = load_courses()

    # Include every valid status, even when no courses currently use it.
    courses_by_status = {
        status: sum(1 for course in courses if course.get("status") == status)
        for status in ("Not Started", "In Progress", "Completed")
    }

    return jsonify(
        {
            "total": len(courses),
            "by_status": courses_by_status,
        }
    ), 200


@app.route("/api/courses/<int:course_id>", methods=["GET"])
def get_course(course_id):
    """Return one course by its numeric ID."""
    with file_lock:
        courses = load_courses()

    course = find_course(courses, course_id)
    if course is None:
        return jsonify({"error": "Course not found."}), 404

    return jsonify(course), 200


@app.route("/api/courses/<int:course_id>", methods=["PUT"])
def update_course(course_id):
    """Replace the editable information for an existing course."""
    data = request.get_json(silent=True)
    error = validate_course_data(data)
    if error:
        return jsonify({"error": error}), 400

    with file_lock:
        courses = load_courses()
        course = find_course(courses, course_id)

        if course is None:
            return jsonify({"error": "Course not found."}), 404

        # The ID and creation timestamp are intentionally kept unchanged.
        course.update(
            {
                "name": data["name"].strip(),
                "description": data["description"].strip(),
                "target_date": data["target_date"],
                "status": data["status"],
            }
        )
        save_courses(courses)

    return jsonify(course), 200


@app.route("/api/courses/<int:course_id>", methods=["DELETE"])
def delete_course(course_id):
    """Delete one course by its numeric ID."""
    with file_lock:
        courses = load_courses()
        course = find_course(courses, course_id)

        if course is None:
            return jsonify({"error": "Course not found."}), 404

        courses.remove(course)
        save_courses(courses)

    return jsonify({"message": "Course deleted successfully."}), 200


if __name__ == "__main__":
    # debug=True is convenient while learning; disable it in production.
    app.run(debug=True)
