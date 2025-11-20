#!/usr/bin/env python3
import earthaccess
from pathlib import Path
from datetime import datetime, timedelta
import calendar
from tqdm import tqdm  # <--- progress bar

# ---------------------------------------------------------------------
# PRODUCT MAPPING
# ---------------------------------------------------------------------
PRODUCT_MAP = {
    "kd":  {"l2": "PACE_OCI_L2_KD",  "l3": "PACE_OCI_L3M_KD_NRT"},
    "chl": {"l2": "PACE_OCI_L2_CHL", "l3": "PACE_OCI_L3M_CHL_NRT"},
    "rrs": {"l2": "PACE_OCI_L2_RRS", "l3": "PACE_OCI_L3M_RRS_NRT"},
    "aop": {"l2": "PACE_OCI_L2_AOP", "l3": "PACE_OCI_L3M_AOP_NRT"},
    "iop": {"l2": "PACE_OCI_L2_IOP", "l3": "PACE_OCI_L3M_IOP_NRT"}
}

# ---------------------------------------------------------------------
# DATE UTILITIES
# ---------------------------------------------------------------------
def daterange(start, end):
    cur = start
    while cur <= end:
        yield cur
        cur += timedelta(days=1)

def monthly_range(start_month, end_month):
    cur = datetime.strptime(start_month, "%Y-%m")
    end = datetime.strptime(end_month, "%Y-%m")
    months = []
    while cur <= end:
        months.append(cur.strftime("%Y-%m"))
        y = cur.year + (cur.month // 12)
        m = (cur.month % 12) + 1
        cur = datetime(y, m, 1)
    return months

# ---------------------------------------------------------------------
# MAIN DOWNLOAD LOGIC
# ---------------------------------------------------------------------
def run_download(args):
    """Core function to download PACE granules based on CLI-like arguments"""
    earthaccess.login(strategy="netrc")
    short_name = PRODUCT_MAP[args.product][args.level]
    SAVE_DIR = Path(args.output)
    SAVE_DIR.mkdir(exist_ok=True, parents=True)

    # build temporal search windows
    date_windows = []
    if args.daily:
        start = datetime.strptime(args.start, "%Y-%m-%d")
        end   = datetime.strptime(args.end, "%Y-%m-%d")
        for d in daterange(start, end):
            date_windows.append((d.strftime("%Y-%m-%d"), d.strftime("%Y-%m-%d")))
    elif args.monthly:
        months = monthly_range(args.start, args.end)
        for ym in months:
            y, m = ym.split("-")
            year = int(y)
            month = int(m)
            start = datetime(year, month, 1)
            last_day = calendar.monthrange(year, month)[1]
            end = datetime(year, month, last_day)
            date_windows.append((start.strftime("%Y-%m-%d"), end.strftime("%Y-%m-%d")))
    else:
        date_windows.append((args.start, args.end))

    for s, e in date_windows:
        print(f"\nSearching {short_name} for {s} → {e}")

        kw = dict(short_name=short_name, temporal=(s, e))
        if args.bbox:
            west, south, east, north = args.bbox
            kw["bounding_box"] = (west, south, east, north)
        if args.point:
            lat, lon = args.point
            kw["point"] = (lon, lat)
            kw["radius"] = args.radius

        granules = earthaccess.search_data(**kw)

        print(f"  Found {len(granules)} granules")
        if len(granules) == 0:
            continue

        print("  Downloading...")
        files = []
        for g in tqdm(granules, desc="Granules", unit="granule"):
            try:
                downloaded = earthaccess.download([g], SAVE_DIR)
                files.extend(downloaded)
            except Exception as ex:
                print(f"    ⚠ Failed to download {g}: {ex}")

        print("  Completed batch:")
        for f in files:
            print("    ✔", f)

    print("\nAll downloads complete.")


# ---------------------------------------------------------------------
# PYTHON API WRAPPERS
# ---------------------------------------------------------------------
def download_monthly(product, level, start_month, end_month, output="./downloads",
                     bbox=None, point=None, radius=50):
    """Download monthly granules via Python API"""
    class Args:
        pass
    args = Args()
    args.product = product
    args.level = level
    args.start = start_month
    args.end = end_month
    args.output = output
    args.bbox = bbox
    args.point = point
    args.radius = radius
    args.daily = False
    args.monthly = True

    Path(output).mkdir(exist_ok=True, parents=True)
    run_download(args)

def download_daily(product, level, start_date, end_date, output="./downloads",
                   bbox=None, point=None, radius=50):
    """Download daily granules via Python API"""
    class Args:
        pass
    args = Args()
    args.product = product
    args.level = level
    args.start = start_date
    args.end = end_date
    args.output = output
    args.bbox = bbox
    args.point = point
    args.radius = radius
    args.daily = True
    args.monthly = False

    Path(output).mkdir(exist_ok=True, parents=True)
    run_download(args)
