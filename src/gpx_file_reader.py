import xml.etree.ElementTree as ET
import xml.dom
import pandas as pd
from datetime import datetime


class GPXFile:
    def __init__(self, gpx_file_path, gpx_schema_doc_site="{http://www.topografix.com/GPX/1/1}"):
        self.gpx_file_path = gpx_file_path
        self.xml_element_prefix = gpx_schema_doc_site
        self.gpx_root = self.get_gpx_root(self.gpx_file_path)
        if self.check_for_time() is True:

            self.gpxColumns = ["lat", "lon", "ele", "time"]
            self.gpxDF = pd.DataFrame(columns=self.gpxColumns)

            self.parse()
        else:
            self.gpxDF = pd.DataFrame({'Empty': []})

    def check_for_time(self):
        track_root = self.gpx_root.find(self.tag("trk"))
        track_segments = track_root.findall(self.tag("trkseg"))
        track_segment = track_segments[0]
        trkpt = track_segment.find(self.tag("trkpt"))
        time_value = trkpt.find(self.tag('time'))
        if time_value is None:
            return False
        else:
            return True

    def get_gpx_root(self, gpx_file_path):
        tree = ET.parse(gpx_file_path)
        root = tree.getroot()
        return root

    def tag(self, tag_name):
        return self.xml_element_prefix + tag_name

    def parse(self):
        track_root = self.gpx_root.find(self.tag("trk"))
        track_segments = track_root.findall(self.tag("trkseg"))

        for i in range(len(track_segments)):
            segRows = []
            track_segment = track_segments[i]
            for trkpt in track_segment:
                latVal = float(trkpt.get("lat"))
                lonVal = float(trkpt.get("lon"))
                eleIter = trkpt.find(self.tag("ele")).itertext()
                elevationVal = float(next(eleIter))
                timeIter = trkpt.find(self.tag("time")).itertext()
                dateTimeStr = datetime.strptime(
                    next(timeIter), '%Y-%m-%dT%H:%M:%SZ')
                segRows.append([latVal, lonVal, elevationVal, dateTimeStr])

            segDF = pd.DataFrame(segRows, columns=self.gpxColumns)
            self.gpxDF = pd.concat([self.gpxDF, segDF], ignore_index=True)

    def get_gpx_dataframe(self):
        return self.gpxDF

    def print_info(self):
        self.gpxDF.info()
        print("preview:\n", self.gpxDF[:10])
