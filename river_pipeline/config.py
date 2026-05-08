"""Configuration objekty pro river-network preprocessing.

Profil odděluje field mapping a dataset-specific defaults od vlastní
processing logiky. Hlavní pipeline díky tomu může používat obecné pojmy jako
flow status, start node, end node nebo region, zatímco konkrétní W05 názvy polí
zůstávají explicitně popsané zde.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Mapping, Sequence


@dataclass(frozen=True)
class RiverSchema:
    """Field mapping pro directed vector river network."""

    flow_status_field: str | None = None
    known_flow_values: tuple[str, ...] = ("1", "TRUE", "T", "YES", "Y")
    start_node_field: str | None = None
    end_node_field: str | None = None
    length_field: str = "LEN_M"
    distance_from_source_field: str = "DIST_SRC_MAX"
    upstream_length_field: str | None = "UPSTR_LEN"
    river_name_field: str | None = None
    river_code_field: str | None = None


@dataclass(frozen=True)
class RegionConfig:
    """Volitelná strategie pro grouping a region metadata."""

    group_label: str = "region"
    code_fields: tuple[str, ...] = ()
    output_code_field: str = "REGION_CODE"
    output_name_field: str = "REGION_NAME"
    code_to_name: Mapping[str, str] = field(default_factory=dict)
    derive_code_from_folder: bool = True


@dataclass(frozen=True)
class PipelineConfig:
    """Dataset profile používaný ve stages discovery, cleaning, metrics a export."""

    name: str
    schema: RiverSchema
    region: RegionConfig | None = None
    stream_keywords: tuple[str, ...] = ("stream", "river", "line")
    node_keywords: tuple[str, ...] = ("node",)
    fallback_crs: str | None = None
    output_prefix: str = "river"
    prefer_file_geodatabase_for_metrics: bool = True


JAPAN_PREFECTURE_NAMES = {
    "01": "Hokkaido",
    "02": "Aomori",
    "03": "Iwate",
    "04": "Miyagi",
    "05": "Akita",
    "06": "Yamagata",
    "07": "Fukushima",
    "08": "Ibaraki",
    "09": "Tochigi",
    "10": "Gunma",
    "11": "Saitama",
    "12": "Chiba",
    "13": "Tokyo",
    "14": "Kanagawa",
    "15": "Niigata",
    "16": "Toyama",
    "17": "Ishikawa",
    "18": "Fukui",
    "19": "Yamanashi",
    "20": "Nagano",
    "21": "Gifu",
    "22": "Shizuoka",
    "23": "Aichi",
    "24": "Mie",
    "25": "Shiga",
    "26": "Kyoto",
    "27": "Osaka",
    "28": "Hyogo",
    "29": "Nara",
    "30": "Wakayama",
    "31": "Tottori",
    "32": "Shimane",
    "33": "Okayama",
    "34": "Hiroshima",
    "35": "Yamaguchi",
    "36": "Tokushima",
    "37": "Kagawa",
    "38": "Ehime",
    "39": "Kochi",
    "40": "Fukuoka",
    "41": "Saga",
    "42": "Nagasaki",
    "43": "Kumamoto",
    "44": "Oita",
    "45": "Miyazaki",
    "46": "Kagoshima",
    "47": "Okinawa",
}


JAPAN_W05_PROFILE = PipelineConfig(
    name="Japan MLIT W05 river network",
    schema=RiverSchema(
        flow_status_field="W05_006",
        start_node_field="W05_009",
        end_node_field="W05_010",
        length_field="LEN_M",
        distance_from_source_field="DIST_SRC_MAX",
        upstream_length_field="UPSTR_LEN",
        river_name_field="W05_004",
        river_code_field="W05_002",
    ),
    region=RegionConfig(
        group_label="prefecture",
        code_fields=("PREF_CODE", "PREFECTURE_CODE", "PREF_CD", "KEN_CD", "KEN_CODE"),
        output_code_field="PREF_CODE",
        output_name_field="PREF_NAME",
        code_to_name=JAPAN_PREFECTURE_NAMES,
    ),
    stream_keywords=("stream", "riverline", "line"),
    node_keywords=("rivernode", "node"),
    fallback_crs="EPSG:4326",
    output_prefix="w05",
)
