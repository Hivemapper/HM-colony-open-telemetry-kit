# Open Telemetry Kit

![Image of Open Telemetry Kit](https://raw.githubusercontent.com/Hivemapper/open-telemetry-kit/master/OTK.jpg)

The Open Telemetry Kit (OTK) is an open source package for extracting and parsing telemetry associated with video streams and converting to common formats.
It comes out of a need for a singular API that can be used for multiple different video telemetry formats.

Telemetry that can be parsed includes: GPS, time, camera information, speed

Features:
- Automatically detect telemetry format
- Manipulate telemetry with ease
- Write telemetry to a new format

## Getting Started
### Dependencies
Python version: `>=3.6`

`ffmpeg` and `ffprobe`.

On Debian systems these can be installed with:
>$ sudo apt install ffmpeg

`dateutil`

On Debian systems this can be installed with:
>$ pip3 install python-dateutil

### Installation
>$ pip3 install open-telemetry-kit

### Importing
The OTK package can be imported into your python3 project with:
>import open_telemetry_kit as otk

### Quick Start
For an example of OTK usage you can download the OTK quickstart package (~90 MB).
This includes a sample `.csv`, `.srt`, and `.mov` with embedded telemetry.
It also contains `quickstart.py` which you can use to extract the telemetry from the sample files.

>$ wget https://hivemapper-sample-videos.s3-us-west-2.amazonaws.com/OTK/OTK_quickstart.tgz

Extract the package:

>$ tar xvf OTK_quickstart.tgz

This will extract everythin into a new directory called `OTK_quickstart/`

The `quickstart.py` script accepts a standalone `.csv` or `.srt` or a video file with an embedded `.srt`. 
It will read in the data, convert it to JSON, and write it to the provided destination. 

From the new OTK_quickstart directory, you can execute the script via one of the following:
>$ python3 quickstart.py srt_example.srt srt_example.json
>$ python3 quickstart.py csv_example.csv csv_example.json
>$ python3 quickstart.py embedded_srt_example.mov embedded_srt_example.json

This process will create a new JSON file containing the telemetry extracted from the sample file.

Note: If the telemetry is embedded (e.g. the third example) this script will also create a `metadata.json` file and extract the data into `[video_name].srt`

For an example of simple data manipulation, open `quickstart.py` and uncomment the lines:

```
# gps = Telemetry()
# for packet in telemetry:
#   gps.append({ k:v for k, v in packet.items() if k in ['latitude', 'longitude', 'altitude']})

# write.telemetryToJson(gps, dest)
```

Then rerun the script with one of the provided commands.

### Current Functionality
#### Input Formats
The OTK currently supports the following forms of telemetry:
- `.csv` files
- `.srt` files
- Any video file with embedded telemetry encoded as a `.srt` (e.g. video taken with some DJI drone models)

#### Output Formats
- JSON

### Future Releases
Planned expansions and updates for the OTK include:

#### Input Formats
- `.kml`
- `.gpx`
- KLV/MISB embedded data

#### Output Formats
- geoJSON

#### Other
- Logging
- Error checking
- Unit Tests
