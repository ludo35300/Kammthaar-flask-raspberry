from flask import jsonify
from flask_jwt_extended import jwt_required
from flask_smorest import Blueprint
from service.mppt_service import MPPTService

mppt_controller = Blueprint('mppt_controller', __name__, url_prefix='/mppt', description="Informations sur le contrôleur MPPT")

@mppt_controller.route('/realtime', methods=['GET'])
@jwt_required()
def get_controller_data():
    service = MPPTService()
    data_controller = service.read_controller_data()
    if data_controller is None:
        return jsonify({"error": "Erreur de communication avec le contrôleur MPPT"}), 500

    return jsonify({
        "controller_temperature": data_controller.controller_temperature,
        "controller_load_voltage": data_controller.controller_load_voltage,
        "controller_load_amperage": data_controller.controller_load_amperage,
        "controller_load_power": data_controller.controller_load_power,
        "is_day": data_controller.controller_day_time,
        "is_night": data_controller.controller_night_time,
        "controller_date": data_controller.controller_date
    }), 200
    
@mppt_controller.route('/charging/status', methods=['GET'])
@jwt_required()
def get_controller_data():
    service = MPPTService()
    data_controller = service.read_charging_status()
    if data_controller is None:
        return jsonify({"error": "Erreur de communication avec le contrôleur MPPT"}), 500

    return jsonify({
        "input_voltage_status": data_controller.input_voltage_status,
        "charging_mosfet_is_short_circuit": data_controller.charging_mosfet_is_short_circuit,
        "charging_or_anti_reverse_mosfet_is_open_circuit": data_controller.charging_or_anti_reverse_mosfet_is_open_circuit,
        "anti_reverse_mosfet_is_short_circuit": data_controller.anti_reverse_mosfet_is_short_circuit,
        "input_over_current": data_controller.input_over_current,
        "load_over_current": data_controller.load_over_current,
        "load_short_circuit": data_controller.controller_date,
        "load_mosfet_short_circuit": data_controller.load_mosfet_short_circuit,
        "disequilibrium_in_three_circuits": data_controller.disequilibrium_in_three_circuits,
        "pv_input_short_circuit": data_controller.pv_input_short_circuit,
        "charging_status": data_controller.charging_status,
        "fault": data_controller.fault,
        "running": data_controller.running
    }), 200

