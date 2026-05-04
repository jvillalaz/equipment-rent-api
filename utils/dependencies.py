from app.persistences.auth_persistence import AuthPersistence
from app.persistences.command_persistence import CommandPersistence
from app.persistences.equipment_persistence import EquipmentPersistence
from app.persistences.reservation_persistence import ReservationPersistence
from app.persistences.user_persistence import UserPersistence
from app.services.auth_service import AuthService
from app.services.command_service import CommandService
from app.services.equipment_service import EquipmentService
from app.services.reservation_service import ReservationService
from app.services.user_service import UserService


def inject_dependencies():
    AuthService(AuthPersistence)
    UserService(UserPersistence)
    EquipmentService(EquipmentPersistence)
    ReservationService(ReservationPersistence, EquipmentPersistence, AuthPersistence, UserPersistence)
    CommandService(CommandPersistence, EquipmentService)
