#!/usr/bin/env python3
import argparse
from .core import run_download

def main():
    parser = argparse.ArgumentParser(description="PACE data downloader using EarthAccess")

    parser.add_argument("--product", required=True,
                        choices=["kd", "chl", "rrs", "aop", "iop"],
                        help="Which PACE variable to download")
    parser.add_argument("--level", required=True,
                        choices=["l2", "l3"],
                        help="L2 or L3 data")
    parser.add_argument("--start", required=True,
                        help="Start date (YYYY-MM-DD or YYYY-MM)")
    parser.add_argument("--end", required=True,
                        help="End date (YYYY-MM-DD or YYYY-MM)")
    parser.add_argument("--output", default="./downloads",
                        help="Output directory")

    # spatial filters
    parser.add_argument("--bbox", nargs=4, type=float,
                        help="Bounding box: west south east north")
    parser.add_argument("--point", nargs=2, type=float,
                        help="Lat lon point")
    parser.add_argument("--radius", type=float, default=50,
                        help="Radius (km) for point search")

    # mode
    parser.add_argument("--daily", action="store_true", help="Download day-by-day")
    parser.add_argument("--monthly", action="store_true", help="Download month-by-month")

    args = parser.parse_args()
    run_download(args)

if __name__ == "__main__":
    main()
