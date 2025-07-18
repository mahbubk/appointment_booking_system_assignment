"""
This module defines the repository and service classes for managing
Skills data access and operations.

It includes:
- GenericRepository: A generic repository for handling CRUD operations
  for any Django model.
- GenericService: A generic service interface for managing operations
  on any model using a repository pattern.
"""


from cfgv import ValidationError

from appointment_booking_system_app.models import Appointment, DoctorProfile, User
from appointment_booking_system_app.repository.generic_repository import (
    GenericRepository,
    GenericService,
)
from appointment_booking_system_app.services.authentication import Authentication
from utils.sql_helper import SqlHelper

auth = Authentication()

sql_helper = SqlHelper()


class DoctorProfileRepository(GenericRepository[DoctorProfile]):
    """Repository for managing DoctorProfile data access and operations."""

    def __init__(self):
        """
        Initialize the DoctorProfile.

        This constructor initializes the repository with the Users model,
        enabling CRUD operations on the DoctorProfile instances.

        It calls the superclasses __init__ method with the DoctorProfile model
        as an argument, allowing the generic repository functionality to be
        applied to the DoctorProfile model specifically.
        """

        super().__init__(DoctorProfile)


class DoctorProfileService(GenericService[DoctorProfile]):
    """
    Service class responsible for handling business logic and operations
    related to Users instances, using the repository layer for
    database interactions.

    This class provides a layer of abstraction over the repository, allowing
    for the enforcement of additional validation rules, data transformations,
    and other business logic. It is designed to be used by application
    components that require access to DoctorProfile data while abstracting away
    direct database operations.

    Key Responsibilities:
    - Retrieve, create, update, and delete Users instances by delegating
      these operations to the Users repository.
    - Implement and enforce business-specific validations and rules, such as
      validating input parameters for retrieval and update operations.
    - Serve as the main access point for DoctorProfile-related operations within
      the application, ensuring consistent handling of Users data.

    Methods:
    - get_by_id: Retrieves a CreditPackage instance by primary key, with validation
      to ensure the key is a positive integer.
    - Additional CRUD methods inherited from GenericService.
    """

    def get_by_id(self, pk: int) -> DoctorProfile | None:
        """Retrieve an instance by primary key with validation."""
        if pk <= 0:
            raise ValidationError("Primary key must be a positive integer.")

        return self.repository.get_by_id(pk)

    @staticmethod
    def get_filter_doctors(filters: dict) -> list[DoctorProfile]:
        """
        Optimized raw SQL query to filter doctors by:
        - Specialization
        - Availability (weekday and time slot)
        - Location (division, district, thana)

        Args:
            filters: Dictionary containing filter parameters:
                - specialization_id (int)
                - weekday (int 0-6)
                - time_slot (time string 'HH:MM')
                - division_id (int)
                - district_id (int)
                - thana_id (int)

        Returns:
            List of doctor profiles as dictionaries
        """
        where_clauses = ["ts.is_available = TRUE"]
        params = []

        if filters.get("division_id"):
            where_clauses.append("d.id = %s")
            params.append(filters["division_id"])
        if filters.get("district_id"):
            where_clauses.append("dist.id = %s")
            params.append(filters["district_id"])
        if filters.get("thana_id"):
            where_clauses.append("t.id = %s")
            params.append(filters["thana_id"])
        if filters.get("specialization_id"):
            where_clauses.append("s.id = %s")
            params.append(filters["specialization_id"])

        where_sql = " AND ".join(where_clauses)
        if where_sql:
            where_sql = "WHERE " + where_sql

        query = f"""
            SELECT DISTINCT dp.*
            FROM appointment_booking_system_app_doctorprofile dp
            JOIN appointment_booking_system_app_specialization s ON dp.specialization_id = s.id
            JOIN appointment_booking_system_app_timeslot ts ON ts.doctor_id = dp.id
            JOIN appointment_booking_system_app_user u ON dp.user_id = u.id
            JOIN appointment_booking_system_app_division d ON u.division_id = d.id
            JOIN appointment_booking_system_app_district dist ON u.district_id = dist.id
            JOIN appointment_booking_system_app_thana t ON u.thana_id = t.id
            {where_sql};
        """

        results = sql_helper.select(query, params)

        return results["data"]

    @staticmethod
    def get_filtered_appointments(filters: dict) -> list[Appointment]:
        """get_filtered_appointments"""
        where_clauses = []
        params = []

        if filters.get("doctor_id"):
            where_clauses.append("a.doctor_id = %s")
            params.append(filters["doctor_id"])

        if filters.get("status"):
            where_clauses.append("a.status = %s")
            params.append(filters["status"])

        if filters.get("start_date"):
            where_clauses.append("a.appointment_date >= %s")
            params.append(filters["start_date"])

        if filters.get("end_date"):
            where_clauses.append("a.appointment_date <= %s")
            params.append(filters["end_date"])

        where_sql = " AND ".join(where_clauses)
        if where_sql:
            where_sql = "WHERE " + where_sql

        query = f"""
               SELECT 
                   a.id,
                   a.patient_id,
                   u.fullname AS patient_name,
                   a.doctor_id,
                   du.fullname AS doctor_name,
                   a.appointment_date,
                   a.appointment_time,
                   a.status,
                   a.consultation_fee,
                   a.notes
               FROM appointment_booking_system_app_appointment a
               LEFT JOIN appointment_booking_system_app_user u ON a.patient_id = u.id
               LEFT JOIN appointment_booking_system_app_doctorprofile dp ON a.doctor_id = dp.id
               LEFT JOIN appointment_booking_system_app_user du ON dp.user_id = du.id
               {where_sql}
               ORDER BY a.appointment_date DESC, a.appointment_time DESC;
           """

        results = sql_helper.select(query, params)

        return results["data"]

    @staticmethod
    def get_user_specific_appointments(user: User) -> Appointment:
        """
        Returns user-specific appointments based on their role.

        - PATIENT: Only their appointments
        - DOCTOR: Appointments linked to their DoctorProfile
        - ADMIN: All appointments
        """
        values = None  # Default in case of ADMIN

        if user.user_type == "PATIENT":
            query = """
                SELECT * FROM appointment_booking_system_app_appointment
                WHERE patient_id = %s
                ORDER BY appointment_date DESC, appointment_time DESC
            """
            values = (user.id,)

        elif user.user_type == "DOCTOR":
            query = """
                SELECT a.*
                FROM appointment_booking_system_app_appointment a
                INNER JOIN appointment_booking_system_app_doctorprofile dp ON a.doctor_id = dp.id
                WHERE dp.user_id = %s
                ORDER BY a.appointment_date DESC, a.appointment_time DESC
            """
            values = (user.id,)

        else:  # ADMIN
            query = """
                SELECT * FROM appointment_booking_system_app_appointment
                ORDER BY appointment_date DESC, appointment_time DESC
            """
            values = None

        results = sql_helper.select(query, values)
        return results["data"]


doctor_profile_repository = DoctorProfileRepository()
doctor_profile_service = DoctorProfileService(doctor_profile_repository)
