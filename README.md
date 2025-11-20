# PACE Downloader

**PACE Downloader** is a command-line and Python API tool for downloading NASA PACE (Plankton, Aerosol, Cloud, ocean Ecosystem) satellite data using EarthAccess API. It supports:

- L2 and L3 products
- Daily or monthly downloads
- Bounding box or point/radius filtering
- Automatic download of all available resolutions

---

## Installation

Clone the repository and install in editable development mode:

### Install via pip in editable mode for development

```bash
git clone https://github.com/devalc/pace-mvp-api.git
cd pace-mvp-api
pip install -e .
```
This installs the CLI command:

```bash
pace-download
```

## 🛰 Supported Products

| Product | Level | Description                         |
|---------|--------|-------------------------------------|
| kd      | L2/L3 | Diffuse attenuation coefficient     |
| chl     | L2/L3 | Chlorophyll                         |
| rrs     | L2/L3 | Remote-sensing reflectance          |
| aop     | L2/L3 | Apparent optical properties         |
| iop     | L2/L3 | Inherent optical properties         |


## Authentication

To run the code successfully, you need to set up authentication with EarthData. Make sure you have your `.netcert` file configured.  

You can follow the official guide here:  
[Earth Access Authentication Guide](https://earthaccess.readthedocs.io/en/stable/howto/authenticate/)

Once your `.netcert` is set up, the code should work as expected.


## 📟 Example: CLI Usage

Download **daily L3 RRS** data for **July 1–2, 2025**, globally:

```bash
pace-download \
  --product rrs \
  --level l3 \
  --daily \
  --start 2025-07-01 \
  --end 2025-07-02 \
  --output ./downloads/rrs_global
```
## 📟 Example: Python API Usage



```python

from pace_downloader.core import download_monthly

download_monthly(
    product="kd",
    level="l3",
    start_month="2024-06",
    end_month="2025-06",
    output="./downloads/kd_monthly"
)
```
