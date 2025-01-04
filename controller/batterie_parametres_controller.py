from flask import jsonify
from flask_jwt_extended import jwt_required
from flask_smorest import Blueprint
from service.batterie_parametres_service import BatterieParametresService

batterie_parametres_controller = Blueprint('batterie_parametres_controller', __name__, url_prefix='/batterie', description="Paramètres de la batterie")

@batterie_parametres_controller.route('/parametres/realtime', methods=['GET'])
@jwt_required()
def get_battery_parametres_data():
    service = BatterieParametresService()
    parametres_battery = service.read_battery_parametres_data()
    if parametres_battery is None:
        return jsonify({"error": "Erreur de communication avec le contrôleur MPPT"}), 500

    return jsonify({
        "rated_charging_current": parametres_battery.rated_charging_current,
        "rated_load_current": parametres_battery.rated_load_current,
        "real_rated_voltage": parametres_battery.real_rated_voltage,
        "battery_type": parametres_battery.battery_type,
        "battery_capacity": parametres_battery.battery_capacity,
        "temp_compensation_coefficient": parametres_battery.temp_compensation_coefficient,
        "over_voltage_disconnect": parametres_battery.over_voltage_disconnect,
        "charging_limit_voltage": parametres_battery.charging_limit_voltage,
        "over_voltage_reconnect": parametres_battery.over_voltage_reconnect,
        "equalize_charging_voltage": parametres_battery.equalize_charging_voltage,
        "boost_charging_voltage": parametres_battery.boost_charging_voltage,
        "float_charging_voltage": parametres_battery.float_charging_voltage,
        "boost_reconnect_voltage": parametres_battery.boost_reconnect_voltage,
        "low_voltage_reconnect": parametres_battery.low_voltage_reconnect,
        "under_voltage_recover": parametres_battery.under_voltage_recover,
        "charging_limit_voltage": parametres_battery.under_voltage_warning,
        "discharging_limit_voltage": parametres_battery.discharging_limit_voltage,
        "battery_rated_voltage": parametres_battery.battery_rated_voltage,
        "default_load_mode": parametres_battery.default_load_mode,
        "equalize_duration": parametres_battery.equalize_duration,
        "boost_duration": parametres_battery.boost_duration,
        "battery_discharge": parametres_battery.battery_discharge,
        "battery_charge": parametres_battery.battery_charge,
        "charging_mode": parametres_battery.charging_mode
    }), 200
