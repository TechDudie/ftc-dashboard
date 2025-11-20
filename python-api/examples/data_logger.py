"""
Data logging example for FTC Dashboard.

This example demonstrates how to log telemetry data to a CSV file
for later analysis.
"""

import asyncio
import csv
import logging
from datetime import datetime
from pathlib import Path
from ftc_dashboard_client import DashboardClient

logging.basicConfig(level=logging.INFO)


class TelemetryLogger:
    """Logger for telemetry data."""
    
    def __init__(self, output_dir="telemetry_logs"):
        self.output_dir = Path(output_dir)
        self.output_dir.mkdir(exist_ok=True)
        
        # Create a timestamped log file
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        self.log_file = self.output_dir / f"telemetry_{timestamp}.csv"
        
        self.csv_writer = None
        self.csv_file = None
        self.headers_written = False
        
    def start(self):
        """Start logging to file."""
        self.csv_file = open(self.log_file, 'w', newline='')
        self.csv_writer = csv.writer(self.csv_file)
        print(f"Logging to: {self.log_file}")
    
    def log_packet(self, packet):
        """Log a single telemetry packet."""
        if not self.csv_writer:
            return
        
        # Write headers if this is the first packet
        if not self.headers_written and packet.data:
            headers = ['timestamp'] + list(packet.data.keys())
            self.csv_writer.writerow(headers)
            self.headers_written = True
            self.csv_file.flush()
        
        # Write data row
        if packet.data:
            row = [packet.timestamp] + list(packet.data.values())
            self.csv_writer.writerow(row)
            self.csv_file.flush()
    
    def stop(self):
        """Stop logging and close file."""
        if self.csv_file:
            self.csv_file.close()
            print(f"Log saved to: {self.log_file}")


async def main():
    # Configuration
    HOST = "192.168.49.1"  # Change to "192.168.43.1" for Control Hub
    PORT = 8000
    DURATION_SECONDS = 30  # How long to log
    
    print("=" * 60)
    print("FTC Dashboard Telemetry Logger")
    print("=" * 60)
    print()
    print(f"Connecting to {HOST}:{PORT}...")
    print(f"Will log data for {DURATION_SECONDS} seconds")
    print()
    
    # Create logger
    logger = TelemetryLogger()
    logger.start()
    
    # Create client
    client = DashboardClient(host=HOST, port=PORT)
    
    packet_count = 0
    
    # Register telemetry handler
    async def on_telemetry(packets):
        nonlocal packet_count
        for packet in packets:
            logger.log_packet(packet)
            packet_count += 1
            
            # Print summary
            if packet.data:
                print(f"Packet {packet_count}: {len(packet.data)} fields")
            
            # Print first packet details
            if packet_count == 1:
                print("\nFirst packet data:")
                for key, value in packet.data.items():
                    print(f"  {key}: {value}")
                print()
    
    client.on_telemetry(on_telemetry)
    
    # Connect and log
    await client.connect()
    
    try:
        print("Logging telemetry data...")
        print("(Press Ctrl+C to stop early)")
        print()
        
        # Run for specified duration
        start_time = asyncio.get_event_loop().time()
        while asyncio.get_event_loop().time() - start_time < DURATION_SECONDS:
            await asyncio.sleep(1)
            elapsed = int(asyncio.get_event_loop().time() - start_time)
            remaining = DURATION_SECONDS - elapsed
            print(f"Progress: {elapsed}s / {DURATION_SECONDS}s ({packet_count} packets logged, {remaining}s remaining)")
        
    except KeyboardInterrupt:
        print("\n\nLogging stopped by user")
    finally:
        await client.disconnect()
        logger.stop()
        
        print()
        print("=" * 60)
        print(f"✓ Logged {packet_count} telemetry packets")
        print("=" * 60)


if __name__ == "__main__":
    asyncio.run(main())
