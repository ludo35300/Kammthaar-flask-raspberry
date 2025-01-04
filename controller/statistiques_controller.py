from flask import jsonify
from flask_jwt_extended import jwt_required
from flask_smorest import Blueprint
from service.statistiques_service import StatistiquesService

statistiques_controller = Blueprint('statistiques_controller', __name__, url_prefix='/statistiques', description="")

@statistiques_controller.route('/realtime', methods=['GET'])
@jwt_required()
def get_statistiques_data():
    service = StatistiquesService()
    data_statistiques = service.read_statistique_data()
    if data_statistiques is None:
        return jsonify({"error": "Erreur de communication avec le contrôleur MPPT"}), 500

    return jsonify({
        "max_battery_voltage_today" : data_statistiques.max_battery_voltage_today,
        "min_battery_voltage_today" : data_statistiques.min_battery_voltage_today,
        "max_ps_voltage_today" : data_statistiques.max_ps_voltage_today,
        "min_ps_voltage_today" : data_statistiques.min_ps_voltage_today,
        "consumed_energy_today" : data_statistiques.consumed_energy_today,
        "consumed_energy_month" : data_statistiques.consumed_energy_month,
        "consumed_energy_year" : data_statistiques.consumed_energy_year,
        "consumed_energy_total" : data_statistiques.consumed_energy_total,
        "generated_energy_today" : data_statistiques.generated_energy_today,
        "generated_energy_month" : data_statistiques.generated_energy_month,
        "generated_energy_year" : data_statistiques.generated_energy_year,
        "generated_energy_total" : data_statistiques.generated_energy_total
    }), 200