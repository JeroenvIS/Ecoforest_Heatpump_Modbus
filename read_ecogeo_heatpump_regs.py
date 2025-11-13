import logging
import csv

from pymodbus.client import ModbusTcpClient as ModbusClient

logger = logging.getLogger(__name__)

if __name__ == "__main__":
    host = "192.168.1.153"
    unitid = 1
    modbus = ModbusClient(host)
    with open('Registers.csv', newline='') as csvfile:
        #  Fetch each register listed in the CSV file
        csv_rows = csv.DictReader(csvfile)
        for row in csv_rows:
            logger.debug(f"{row}")
            regtype = row.get('Type', '')
            units = row.get('Units', '')
            descr = row.get('Description', '')
            remarks = row.get('Remarks', '')
            register = int(row.get('BMS Address'))
            result = 0
            if regtype == 'Coil':
                r = modbus.read_coils(register)
                result = int(r.bits[0])
            else:
                r = modbus.read_holding_registers(register)
                result = r.registers[0]
                if regtype == 'Analog':
                    result /= 10
            print(f"{regtype} register {register:4d}: {result:6} {units:<4} {descr}; Remarks: {remarks}")

