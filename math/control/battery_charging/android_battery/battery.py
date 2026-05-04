# -*- coding: utf-8 -*-

import numpy as np

class BatteryInfo:
    def __init__(self, name):
        with open(name, encoding="latin1") as fd:
            self.contents = fd.read()

        self.contents = self.contents.split("-*-\n")[1:]
        self.contents = [c.strip() for c in self.contents]

    def _get_raw_field(self, field):
        """Get content of the field from /sys/class/power_supply/battery/*"""
        time = []
        output = []
        for i in range(1, len(self.contents), 3):
            if self.contents[i].split("/")[-1] == field:
                time.append((float(self.contents[i - 1]) - float(self.contents[0])))
                try:
                    output.append(float(self.contents[i + 1]))
                except (ValueError, TypeError):
                    output.append(self.contents[i + 1])

        time = np.asarray(time)
        output = np.asarray(output)
        return time, output

    def get_field(self, field, rm_dupes=True):
        """Only return the portion of the data when the battery is being charged."""
        t, status = self._get_raw_field("status")
        ii = np.where(status == "Charging")[0]
        t_min = t[ii[0]]
        t_max = t[ii[-1]]

        t_out, out = self._get_raw_field(field)
        out = out[(t_out >= t_min) & (t_out <= t_max)]
        t_out = t_out[(t_out >= t_min) & (t_out <= t_max)]

        t_soc, soc = self._get_raw_field("capacity")
        soc = soc[(t_soc >= t_min) & (t_soc <= t_max)]
        t_soc = t_soc[(t_soc >= t_min) & (t_soc <= t_max)]

        size = min(len(t_soc), len(t_out), len(soc), len(out))
        if rm_dupes:
            return self.remove_duplicates(t_out[:size], soc[:size], out[:size])
        else:
            return t_out[:size], soc[:size], out[:size]

    @staticmethod
    def remove_duplicates(t, soc, out):
        unique_soc, inv = np.unique(soc, return_inverse=True)
        N = len(unique_soc)

        out_avg = np.empty(N)
        t_avg = np.empty(N)
        # The SOC is integer-valued.  So, we average t and out to get
        # unique values for each SOC.
        for i in range(N):
            out_avg[i] = out[inv == i].mean()
            t_avg[i] = t[inv == i].mean()

        # Time starts from 0.
        t_avg -= t_avg[0]

        return t_avg, unique_soc, out_avg

# Fields
# ------
#
# https://docs.kernel.org/power/power_supply_class.html
#
#     All voltages, currents, charges, energies, time and temperatures in µV, µA, µAh, µWh, seconds
#     and tenths of degree Celsius unless otherwise stated. It’s driver’s job to convert its raw
#     values to units in which this class operates.
#
# aacc
# aacp_version
# aacr_algo
# aacr_cliff_capacity_rate
# aacr_cycle_grace
# aacr_cycle_max
# aacr_min_capacity_rate
# aacr_profile
# aacr_state
# aact_state
# aafv_apply_max
# aafv_cliff_cycle
# aafv_cliff_offset
# aafv_max_offset
# aafv_offset
# aafv_profile
# aafv_state
# ac_soc
# bd_clear
# bd_trickle_cnt
# bd_trickle_dry_run
# bd_trickle_enable
# bd_trickle_recharge_soc
# bd_trickle_reset_sec
# capacity
# capacity_level
# charge_counter
# charge_deadline
# charge_deadline_dryrun
# charge_details
# charge_full
# charge_full_design
# charge_full_estimate
# charge_limit
# charge_stage
# charge_stats
# charge_stats_actual
# charge_to_limit
# charge_type
# charger_state
# charging_policy
# charging_speed
# charging_state
# chg_profile_switch
# constant_charge_current
# constant_charge_voltage
# csi_stats
# current_avg
# current_now
# cycle_count
# cycle_counts
# dev_sn
# first_usage_date
# health
# health_algo
# health_capacity_index
# health_get_cal_state
# health_impedance_index
# health_index
# health_index_stats
# health_indi_cap
# health_safety_margin
# health_set_cal_mode
# health_status
# manufacturing_date
# pairing_state
# power_metrics_current
# power_metrics_interval
# power_metrics_polling_rate
# power_metrics_power
# present
# resistance
# resistance_avg
# serial_number
# ssoc_details
# status # Charging or Discharging
# swelling_data
# technology
# temp
# temp_filter_enable
# time_to_ac
# time_to_empty_avg
# time_to_full_now
# ttf_details
# ttf_stats
# type
# uevent
# voltage_now
# voltage_ocv
