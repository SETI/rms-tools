################################################################################
# textkernel.py
#
# This is a set of routines for parsing SPICE text kernels. It returns a
# dictionary of all the parameters and their values. It implements the complete
# syntax specification as discussed in the SPICE Kernel Required Reading
# document, "kernel.req". However, it cannot be guaranteed that the parsing of
# date/time fields is identical, although dates that are unambiguous should be
# treated the same.
#
# Method:
#   textkernel.FromFile(filename, clear=True)
#
# Input:
#   filename        the name of a text file.
#   clear           True to return the contents of this text kernel only;
#                   False to return a dictionary in which the contents of the
#                   prior call(s) to FromFile() have been merged with the new
#                   entries.
#
# Return:           A dictionary.
#
# Note that the returned dictionary is keyed in a very specific way based on the
# structure of the keyword names in the kernel. Examples:
#   BODY399_POLE_RA     dict["BODY"][399]["POLE_RA"]
#   MESSAGE             dict["MESSAGE"]
#   DELTET/EB           dict["DELTET"]["EB"]
#   FRAME_624_NAME      dict["FRAME"][624]["NAME"]
#
# Also, frames and bodies can be referenced by their name or their numeric ID.
# These are equivalent:
#   dict["FRAME"][623]      dict["FRAME"]["IAU_SUTTUNGR"]
#   dict["BODY"][399]       dict["BODY"]["SATURN"]
#
# Frame and body dictionaries also have an additional keyword "ID" added, which
# returns the numeric ID and is useful when the dictionary is selected by name
# instead. Example:
#   dict["FRAME"]["IAU_SUTTUNGR"]["ID"] = 623
#   dict["FRAME"][623]["ID"] = 623
#
# Mark R. Showalter
# PDS Rings Node
# August 2011
################################################################################

from pyparsing import *
import julian
import datetime as dt
import unittest

global DICTIONARY
DICTIONARY = {}

################################################################################
# Pre-defined BODY names and IDs from ZZIDMAP.F
################################################################################

PREDEFINED_BODY_ID_FROM_NAME = {"SSB":0, "SOLAR SYSTEM BARYCENTER":0,
    "MERCURY BARYCENTER":1, "VENUS BARYCENTER":2, "EMB":3,
    "EARTH MOON BARYCENTER":3, "EARTH-MOON BARYCENTER":3, "EARTH BARYCENTER":3,
    "MARS BARYCENTER":4, "JUPITER BARYCENTER":5, "SATURN BARYCENTER":6,
    "URANUS BARYCENTER":7, "NEPTUNE BARYCENTER":8, "PLUTO BARYCENTER":9,
    "SUN":10, "MERCURY":199, "VENUS":299, "EARTH":399, "MOON":301, "MARS":499,
    "PHOBOS":401, "DEIMOS":402, "JUPITER":599, "IO":501, "EUROPA":502,
    "GANYMEDE":503, "CALLISTO":504, "AMALTHEA":505, "HIMALIA":506, "ELARA":507,
    "PASIPHAE":508, "SINOPE":509, "LYSITHEA":510, "CARME":511, "ANANKE":512,
    "LEDA":513, "THEBE":514, "ADRASTEA":515, "METIS":516, "CALLIRRHOE":517,
    "THEMISTO":518, "MAGACLITE":519, "TAYGETE":520, "CHALDENE":521,
    "HARPALYKE":522, "KALYKE":523, "IOCASTE":524, "ERINOME":525, "ISONOE":526,
    "PRAXIDIKE":527, "AUTONOE":528, "THYONE":529, "HERMIPPE":530, "AITNE":531,
    "EURYDOME":532, "EUANTHE":533, "EUPORIE":534, "ORTHOSIE":535, "SPONDE":536,
    "KALE":537, "PASITHEE":538, "HEGEMONE":539, "MNEME":540, "AOEDE":541,
    "THELXINOE":542, "ARCHE":543, "KALLICHORE":544, "HELIKE":545, "CARPO":546,
    "EUKELADE":547, "CYLLENE":548, "KORE":549, "HERSE":550, "SATURN":699,
    "MIMAS":601, "ENCELADUS":602, "TETHYS":603, "DIONE":604, "RHEA":605,
    "TITAN":606, "HYPERION":607, "IAPETUS":608, "PHOEBE":609, "JANUS":610,
    "EPIMETHEUS":611, "HELENE":612, "TELESTO":613, "CALYPSO":614, "ATLAS":615,
    "PROMETHEUS":616, "PANDORA":617, "PAN":618, "YMIR":619, "PAALIAQ":620,
    "TARVOS":621, "IJIRAQ":622, "SUTTUNGR":623, "KIVIUQ":624, "MUNDILFARI":625,
    "ALBIORIX":626, "SKATHI":627, "ERRIAPUS":628, "SIARNAQ":629, "THRYMR":630,
    "NARVI":631, "METHONE":632, "PALLENE":633, "POLYDEUCES":634, "DAPHNIS":635,
    "AEGIR":636, "BEBHIONN":637, "BERGELMIR":638, "BESTLA":639, "FARBAUTI":640,
    "FENRIR":641, "FORNJOT":642, "HATI":643, "HYROKKIN":644, "KARI":645,
    "LOGE":646, "SKOLL":647, "SURTUR":648, "ANTHE":649, "JARNSAXA":650,
    "GREIP":651, "TARQEQ":652, "AEGAEON":653, "URANUS":799, "ARIEL":701,
    "UMBRIEL":702, "TITANIA":703, "OBERON":704, "MIRANDA":705, "CORDELIA":706,
    "OPHELIA":707, "BIANCA":708, "CRESSIDA":709, "DESDEMONA":710, "JULIET":711,
    "PORTIA":712, "ROSALIND":713, "BELINDA":714, "PUCK":715, "CALIBAN":716,
    "SYCORAX":717, "PROSPERO":718, "SETEBOS":719, "STEPHANO":720,
    "TRINCULO":721, "FRANCISCO":722, "MARGARET":723, "FERDINAND":724,
    "PERDITA":725, "MAB":726, "CUPID":727, "NEPTUNE":899, "TRITON":801,
    "NEREID":802, "NAIAD":803, "THALASSA":804, "DESPINA":805, "GALATEA":806,
    "LARISSA":807, "PROTEUS":808, "HALIMEDE":809, "PSAMATHE":810, "SAO":811,
    "LAOMEDEIA":812, "NESO":813, "PLUTO":999, "CHARON":901, "NIX":902,
    "HYDRA":903,
    "GEOTAIL":-1, "AKATSUKI":-5, "VCO":-5, "PLC":-5, "PLANET-C":-5, "P6":-6,
    "PIONEER-6":-6, "P7":-7, "PIONEER-7":-7, "WIND":-8, "VENUS ORBITER":-12,
    "P12":-12, "PIONEER 12":-12, "POLAR":-13, "MGN":-18, "MAGELLAN":-18,
    "LCROSS":-18, "P8":-20, "PIONEER-8":-20, "SOHO":-21, "P10":-23,
    "PIONEER-10":-23, "P11":-24, "PIONEER-11":-24, "LP":-25,
    "LUNAR PROSPECTOR":-25, "VK1":-27, "VIKING 1 ORBITER":-27, "STARDUST":-29,
    "SDU":-29, "NEXT":-29, "VK2":-30, "VIKING 2 ORBITER":-30, "DS-1":-30,
    "VG1":-31, "VOYAGER 1":-31, "VG2":-32, "VOYAGER 2":-32, "CLEMENTINE":-40,
    "MEX":-41, "MARS EXPRESS":-41, "BEAGLE2":-44, "BEAGLE 2":-44, "MS-T5":-46,
    "SAKIGAKE":-46, "PLANET-A":-47, "SUISEI":-47, "GNS":-47, "GENESIS":-47,
    "HUBBLE SPACE TELESCOPE":-48, "HST":-48, "MARS PATHFINDER":-53, "MPF":-53,
    "MARS ODYSSEY":-53, "MARS SURVEYOR 01 ORBITER":-53, "ULYSSES":-55,
    "VSOP":-58, "HALCA":-58, "RADIOASTRON":-59, "JUNO":-61, "VEGA 1":-66,
    "VEGA 2":-67, "MMO":-68, "MERCURY MAGNETOSPHERIC ORBITER":-68, "MPO":-69,
    "MERCURY PLANETARY ORBITER":-69, "DEEP IMPACT IMPACTOR SPACECRAFT":-70,
    "MRO":-74, "MARS RECON ORBITER":-74, "MSL":-76,
    "MARS SCIENCE LABORATORY":-76, "GLL":-77, "GALILEO ORBITER":-77,
    "GIOTTO":-78, "SPITZER":-79, "SPACE INFRARED TELESCOPE FACILITY":-79,
    "SIRTF":-79, "CASSINI ITL":-81, "CAS":-82, "CASSINI":-82, "PHOENIX":-84,
    "LRO":-85, "LUNAR RECON ORBITER":-85, "LUNAR RECONNAISSANCE ORBITER":-85,
    "CH1":-86, "CHANDRAYAAN-1":-86, "CASSINI SIMULATION":-90,
    "NEAR EARTH ASTEROID RENDEZVOUS":-93, "NEAR":-93, "MO":-94,
    "MARS OBSERVER":-94, "MGS":-94, "MARS GLOBAL SURVEYOR":-94,
    "MGS SIMULATION":-95, "TOPEX/POSEIDON":-97, "NEW HORIZONS":-98,
    "TROPICAL RAINFALL MEASURING MISSION":-107, "TRMM":-107, "ICE":-112,
    "MARS POLAR LANDER":-116, "MPL":-116, "BEPICOLOMBO":-121,
    "MARS CLIMATE ORBITER":-127, "MCO":-127, "MUSES-C":-130, "HAYABUSA":-130,
    "SELENE":-131, "KAGUYA":-131, "DRTS-W":-135, "EPOCH":-140, "DIXI":-140,
    "EPOXI":-140, "DEEP IMPACT FLYBY SPACECRAFT":-140, "TERRA":-142,
    "EOS-AM1":-142, "LUNAR-A":-146, "CASSINI PROBE":-150, "HUYGENS PROBE":-150,
    "CASP":-150, "AXAF":-151, "CHANDRA":-151, "AQUA":-154,
    "EUROPA ORBITER":-159, "YOHKOH":-164, "SOLAR-A":-164, "MAP":-165,
    "IMAGE":-166, "GRAIL-A":-177, "PLANET-B":-178, "NOZOMI":-178,
    "GRAIL-B":-181, "CLUSTER 1":-183, "CLUSTER 2":-185, "SOLAR PROBE":-187,
    "MUSES-B":-188, "SIM":-190, "CLUSTER 3":-194, "CLUSTER 4":-196,
    "INTEGRAL":-198, "CONTOUR":-200, "MAVEN":-202, "DAWN":-203,
    "SOIL MOISTURE ACTIVE AND PASSIVE":-205, "SMAP":-205, "STV51":-212,
    "STV52":-213, "STV53":-214, "ROSETTA":-226, "KEPLER":-227, "GLL PROBE":-228,
    "GALILEO PROBE":-228, "STEREO AHEAD":-234, "STEREO BEHIND":-235,
    "MESSENGER":-236, "SMART1":-238, "SM1":-238, "S1":-238, "SMART-1":-238,
    "VEX":-248, "VENUS EXPRESS":-248, "OPPORTUNITY":-253, "MER-1":-253,
    "SPIRIT":-254, "MER-2":-254, "RADIATION BELT STORM PROBE A":-362,
    "RBSP_A":-362, "RADIATION BELT STORM PROBE B":-363, "RBSP_B":-363,
    "HERSCHEL":-486, "PLANCK":-489, "RSAT":-500, "SELENE RELAY SATELLITE":-500,
    "SELENE RSTAR":-500, "RSTAR":-500, "VSAT":-502,
    "SELENE VLBI RADIO SATELLITE":-502, "SELENE VRAD SATELLITE":-502,
    "SELENE VSTAR":-502, "VSTAR":-502, "MARS-96":-550, "M96":-550,
    "MARS 96":-550, "MARS96":-550,
    "SHOEMAKER-LEVY 9-W":50000001, "SHOEMAKER-LEVY 9-V":50000002,
    "SHOEMAKER-LEVY 9-U":50000003, "SHOEMAKER-LEVY 9-T":50000004,
    "SHOEMAKER-LEVY 9-S":50000005, "SHOEMAKER-LEVY 9-R":50000006,
    "SHOEMAKER-LEVY 9-Q":50000007, "SHOEMAKER-LEVY 9-P":50000008,
    "SHOEMAKER-LEVY 9-N":50000009, "SHOEMAKER-LEVY 9-M":50000010,
    "SHOEMAKER-LEVY 9-L":50000011, "SHOEMAKER-LEVY 9-K":50000012,
    "SHOEMAKER-LEVY 9-J":50000013, "SHOEMAKER-LEVY 9-H":50000014,
    "SHOEMAKER-LEVY 9-G":50000015, "SHOEMAKER-LEVY 9-F":50000016,
    "SHOEMAKER-LEVY 9-E":50000017, "SHOEMAKER-LEVY 9-D":50000018,
    "SHOEMAKER-LEVY 9-C":50000019, "SHOEMAKER-LEVY 9-B":50000020,
    "SHOEMAKER-LEVY 9-A":50000021, "SHOEMAKER-LEVY 9-Q1":50000022,
    "SHOEMAKER-LEVY 9-P2":50000023, "AREND":1000001, "AREND-RIGAUX":1000002,
    "ASHBROOK-JACKSON":1000003, "BOETHIN":1000004, "BORRELLY":1000005,
    "BOWELL-SKIFF":1000006, "BRADFIELD":1000007, "BROOKS 2":1000008,
    "BRORSEN-METCALF":1000009, "BUS":1000010, "CHERNYKH":1000011,
    "67P/CHURYUMOV-GERASIMENKO (1969 R1)":1000012,
    "CHURYUMOV-GERASIMENKO":1000012, "CIFFREO":1000013, "CLARK":1000014,
    "COMAS SOLA":1000015, "CROMMELIN":1000016, "D''ARREST":1000017,
    "DANIEL":1000018, "DE VICO-SWIFT":1000019, "DENNING-FUJIKAWA":1000020,
    "DU TOIT 1":1000021, "DU TOIT-HARTLEY":1000022,
    "DUTOIT-NEUJMIN-DELPORTE":1000023, "DUBIAGO":1000024, "ENCKE":1000025,
    "FAYE":1000026, "FINLAY":1000027, "FORBES":1000028, "GEHRELS 1":1000029,
    "GEHRELS 2":1000030, "GEHRELS 3":1000031, "GIACOBINI-ZINNER":1000032,
    "GICLAS":1000033, "GRIGG-SKJELLERUP":1000034, "GUNN":1000035,
    "HALLEY":1000036, "HANEDA-CAMPOS":1000037, "HARRINGTON":1000038,
    "HARRINGTON-ABELL":1000039, "HARTLEY 1":1000040, "HARTLEY 2":1000041,
    "HARTLEY-IRAS":1000042, "HERSCHEL-RIGOLLET":1000043, "HOLMES":1000044,
    "HONDA-MRKOS-PAJDUSAKOVA":1000045, "HOWELL":1000046, "IRAS":1000047,
    "JACKSON-NEUJMIN":1000048, "JOHNSON":1000049, "KEARNS-KWEE":1000050,
    "KLEMOLA":1000051, "KOHOUTEK":1000052, "KOJIMA":1000053, "KOPFF":1000054,
    "KOWAL 1":1000055, "KOWAL 2":1000056, "KOWAL-MRKOS":1000057,
    "KOWAL-VAVROVA":1000058, "LONGMORE":1000059, "LOVAS 1":1000060,
    "MACHHOLZ":1000061, "MAURY":1000062, "NEUJMIN 1":1000063,
    "NEUJMIN 2":1000064, "NEUJMIN 3":1000065, "OLBERS":1000066,
    "PETERS-HARTLEY":1000067, "PONS-BROOKS":1000068, "PONS-WINNECKE":1000069,
    "REINMUTH 1":1000070, "REINMUTH 2":1000071, "RUSSELL 1":1000072,
    "RUSSELL 2":1000073, "RUSSELL 3":1000074, "RUSSELL 4":1000075,
    "SANGUIN":1000076, "SCHAUMASSE":1000077, "SCHUSTER":1000078,
    "SCHWASSMANN-WACHMANN 1":1000079, "SCHWASSMANN-WACHMANN 2":1000080,
    "SCHWASSMANN-WACHMANN 3":1000081, "SHAJN-SCHALDACH":1000082,
    "SHOEMAKER 1":1000083, "SHOEMAKER 2":1000084, "SHOEMAKER 3":1000085,
    "SINGER-BREWSTER":1000086, "SLAUGHTER-BURNHAM":1000087,
    "SMIRNOVA-CHERNYKH":1000088, "STEPHAN-OTERMA":1000089,
    "SWIFT-GEHRELS":1000090, "TAKAMIZAWA":1000091, "TAYLOR":1000092,
    "TEMPEL_1":1000093, "TEMPEL 1":1000093, "TEMPEL 2":1000094,
    "TEMPEL-TUTTLE":1000095, "TRITTON":1000096, "TSUCHINSHAN 1":1000097,
    "TSUCHINSHAN 2":1000098, "TUTTLE":1000099,
    "TUTTLE-GIACOBINI-KRESAK":1000100, "VAISALA 1":1000101,
    "VAN BIESBROECK":1000102, "VAN HOUTEN":1000103,
    "WEST-KOHOUTEK-IKEMURA":1000104, "WHIPPLE":1000105, "WILD 1":1000106,
    "WILD 2":1000107, "WILD 3":1000108, "WIRTANEN":1000109, "WOLF":1000110,
    "WOLF-HARRINGTON":1000111, "LOVAS 2":1000112, "URATA-NIIJIMA":1000113,
    "WISEMAN-SKIFF":1000114, "HELIN":1000115, "MUELLER":1000116,
    "SHOEMAKER-HOLT 1":1000117, "HELIN-ROMAN-CROCKETT":1000118,
    "HARTLEY 3":1000119, "PARKER-HARTLEY":1000120, "HELIN-ROMAN-ALU 1":1000121,
    "WILD 4":1000122, "MUELLER 2":1000123, "MUELLER 3":1000124,
    "SHOEMAKER-LEVY 1":1000125, "SHOEMAKER-LEVY 2":1000126,
    "HOLT-OLMSTEAD":1000127, "METCALF-BREWINGTON":1000128, "LEVY":1000129,
    "SHOEMAKER-LEVY 9":1000130, "HYAKUTAKE":1000131, "HALE-BOPP":1000132,
    "GASPRA":9511010, "IDA":2431010, "DACTYL":2431011, "CERES":2000001,
    "VESTA":2000004, "LUTETIA":2000021, "KLEOPATRA":2000216, "EROS":2000433,
    "MATHILDE":2000253, "STEINS":2002867, "1992KD":2009969, "BRAILLE":2009969,
    "WILSON-HARRINGTON":2004015, "TOUTATIS":2004179, "ITOKAWA":2025143,
    "NOTO":398989, "NEW NORCIA":398990, "GOLDSTONE":399001, "CANBERRA":399002,
    "MADRID":399003, "USUDA":399004, "DSS-05":399005, "PARKES":399005,
    "DSS-12":399012, "DSS-13":399013, "DSS-14":399014, "DSS-15":399015,
    "DSS-16":399016, "DSS-17":399017, "DSS-23":399023, "DSS-24":399024,
    "DSS-25":399025, "DSS-26":399026, "DSS-27":399027, "DSS-28":399028,
    "DSS-33":399033, "DSS-34":399034, "DSS-42":399042, "DSS-43":399043,
    "DSS-45":399045, "DSS-46":399046, "DSS-49":399049, "DSS-53":399053,
    "DSS-54":399054, "DSS-55":399055, "DSS-61":399061, "DSS-63":399063,
    "DSS-64":399064, "DSS-65":399065, "DSS-66":399066}

# At load time, create a backwards dictionary to look up body name from ID

PREDEFINED_BODY_NAME_FROM_ID = {}
for key in PREDEFINED_BODY_ID_FROM_NAME.keys():
    id = PREDEFINED_BODY_ID_FROM_NAME[key]
    PREDEFINED_BODY_NAME_FROM_ID[id] = key

################################################################################
# Pre-defined FRAME names, IDs and central bodies from ZZFDAT.F
################################################################################

PREDEFINED_FRAME_INFO = {
    10001:{"ID":10001, "CENTER":1, "NAME":"IAU_MERCURY_BARYCENTER"},
    10002:{"ID":10002, "CENTER":2, "NAME":"IAU_VENUS_BARYCENTER"},
    10003:{"ID":10003, "CENTER":3, "NAME":"IAU_EARTH_BARYCENTER"},
    10004:{"ID":10004, "CENTER":4, "NAME":"IAU_MARS_BARYCENTER"},
    10005:{"ID":10005, "CENTER":5, "NAME":"IAU_JUPITER_BARYCENTER"},
    10006:{"ID":10006, "CENTER":6, "NAME":"IAU_SATURN_BARYCENTER"},
    10007:{"ID":10007, "CENTER":7, "NAME":"IAU_URANUS_BARYCENTER"},
    10008:{"ID":10008, "CENTER":8, "NAME":"IAU_NEPTUNE_BARYCENTER"},
    10009:{"ID":10009, "CENTER":9, "NAME":"IAU_PLUTO_BARYCENTER"},
    10010:{"ID":10010, "CENTER":10, "NAME":"IAU_SUN"},
    10011:{"ID":10011, "CENTER":199, "NAME":"IAU_MERCURY"},
    10012:{"ID":10012, "CENTER":299, "NAME":"IAU_VENUS"},
    10013:{"ID":10013, "CENTER":399, "NAME":"IAU_EARTH"},
    10014:{"ID":10014, "CENTER":499, "NAME":"IAU_MARS"},
    10015:{"ID":10015, "CENTER":599, "NAME":"IAU_JUPITER"},
    10016:{"ID":10016, "CENTER":699, "NAME":"IAU_SATURN"},
    10017:{"ID":10017, "CENTER":799, "NAME":"IAU_URANUS"},
    10018:{"ID":10018, "CENTER":899, "NAME":"IAU_NEPTUNE"},
    10019:{"ID":10019, "CENTER":999, "NAME":"IAU_PLUTO"},
    10020:{"ID":10020, "CENTER":301, "NAME":"IAU_MOON"},
    10021:{"ID":10021, "CENTER":401, "NAME":"IAU_PHOBOS"},
    10022:{"ID":10022, "CENTER":402, "NAME":"IAU_DEIMOS"},
    10023:{"ID":10023, "CENTER":501, "NAME":"IAU_IO"},
    10024:{"ID":10024, "CENTER":502, "NAME":"IAU_EUROPA"},
    10025:{"ID":10025, "CENTER":503, "NAME":"IAU_GANYMEDE"},
    10026:{"ID":10026, "CENTER":504, "NAME":"IAU_CALLISTO"},
    10027:{"ID":10027, "CENTER":505, "NAME":"IAU_AMALTHEA"},
    10028:{"ID":10028, "CENTER":506, "NAME":"IAU_HIMALIA"},
    10029:{"ID":10029, "CENTER":507, "NAME":"IAU_ELARA"},
    10030:{"ID":10030, "CENTER":508, "NAME":"IAU_PASIPHAE"},
    10031:{"ID":10031, "CENTER":509, "NAME":"IAU_SINOPE"},
    10032:{"ID":10032, "CENTER":510, "NAME":"IAU_LYSITHEA"},
    10033:{"ID":10033, "CENTER":511, "NAME":"IAU_CARME"},
    10034:{"ID":10034, "CENTER":512, "NAME":"IAU_ANANKE"},
    10035:{"ID":10035, "CENTER":513, "NAME":"IAU_LEDA"},
    10036:{"ID":10036, "CENTER":514, "NAME":"IAU_THEBE"},
    10037:{"ID":10037, "CENTER":515, "NAME":"IAU_ADRASTEA"},
    10038:{"ID":10038, "CENTER":516, "NAME":"IAU_METIS"},
    10039:{"ID":10039, "CENTER":601, "NAME":"IAU_MIMAS"},
    10040:{"ID":10040, "CENTER":602, "NAME":"IAU_ENCELADUS"},
    10041:{"ID":10041, "CENTER":603, "NAME":"IAU_TETHYS"},
    10042:{"ID":10042, "CENTER":604, "NAME":"IAU_DIONE"},
    10043:{"ID":10043, "CENTER":605, "NAME":"IAU_RHEA"},
    10044:{"ID":10044, "CENTER":606, "NAME":"IAU_TITAN"},
    10045:{"ID":10045, "CENTER":607, "NAME":"IAU_HYPERION"},
    10046:{"ID":10046, "CENTER":608, "NAME":"IAU_IAPETUS"},
    10047:{"ID":10047, "CENTER":609, "NAME":"IAU_PHOEBE"},
    10048:{"ID":10048, "CENTER":610, "NAME":"IAU_JANUS"},
    10049:{"ID":10049, "CENTER":611, "NAME":"IAU_EPIMETHEUS"},
    10050:{"ID":10050, "CENTER":612, "NAME":"IAU_HELENE"},
    10051:{"ID":10051, "CENTER":613, "NAME":"IAU_TELESTO"},
    10052:{"ID":10052, "CENTER":614, "NAME":"IAU_CALYPSO"},
    10053:{"ID":10053, "CENTER":615, "NAME":"IAU_ATLAS"},
    10054:{"ID":10054, "CENTER":616, "NAME":"IAU_PROMETHEUS"},
    10055:{"ID":10055, "CENTER":617, "NAME":"IAU_PANDORA"},
    10056:{"ID":10056, "CENTER":701, "NAME":"IAU_ARIEL"},
    10057:{"ID":10057, "CENTER":702, "NAME":"IAU_UMBRIEL"},
    10058:{"ID":10058, "CENTER":703, "NAME":"IAU_TITANIA"},
    10059:{"ID":10059, "CENTER":704, "NAME":"IAU_OBERON"},
    10060:{"ID":10060, "CENTER":705, "NAME":"IAU_MIRANDA"},
    10061:{"ID":10061, "CENTER":706, "NAME":"IAU_CORDELIA"},
    10062:{"ID":10062, "CENTER":707, "NAME":"IAU_OPHELIA"},
    10063:{"ID":10063, "CENTER":708, "NAME":"IAU_BIANCA"},
    10064:{"ID":10064, "CENTER":709, "NAME":"IAU_CRESSIDA"},
    10065:{"ID":10065, "CENTER":710, "NAME":"IAU_DESDEMONA"},
    10066:{"ID":10066, "CENTER":711, "NAME":"IAU_JULIET"},
    10067:{"ID":10067, "CENTER":712, "NAME":"IAU_PORTIA"},
    10068:{"ID":10068, "CENTER":713, "NAME":"IAU_ROSALIND"},
    10069:{"ID":10069, "CENTER":714, "NAME":"IAU_BELINDA"},
    10070:{"ID":10070, "CENTER":715, "NAME":"IAU_PUCK"},
    10071:{"ID":10071, "CENTER":801, "NAME":"IAU_TRITON"},
    10072:{"ID":10072, "CENTER":802, "NAME":"IAU_NEREID"},
    10073:{"ID":10073, "CENTER":803, "NAME":"IAU_NAIAD"},
    10074:{"ID":10074, "CENTER":804, "NAME":"IAU_THALASSA"},
    10075:{"ID":10075, "CENTER":805, "NAME":"IAU_DESPINA"},
    10076:{"ID":10076, "CENTER":806, "NAME":"IAU_GALATEA"},
    10077:{"ID":10077, "CENTER":807, "NAME":"IAU_LARISSA"},
    10078:{"ID":10078, "CENTER":808, "NAME":"IAU_PROTEUS"},
    10079:{"ID":10079, "CENTER":901, "NAME":"IAU_CHARON"},
    10081:{"ID":10081, "CENTER":399, "NAME":"EARTH_FIXED"},
    10082:{"ID":10082, "CENTER":618, "NAME":"IAU_PAN"},
    10083:{"ID":10083, "CENTER":9511010, "NAME":"IAU_GASPRA"},
    10084:{"ID":10084, "CENTER":2431010, "NAME":"IAU_IDA"},
    10085:{"ID":10085, "CENTER":2000433, "NAME":"IAU_EROS"},
    10086:{"ID":10086, "CENTER":517, "NAME":"IAU_CALLIRRHOE"},
    10087:{"ID":10087, "CENTER":518, "NAME":"IAU_THEMISTO"},
    10088:{"ID":10088, "CENTER":519, "NAME":"IAU_MAGACLITE"},
    10089:{"ID":10089, "CENTER":520, "NAME":"IAU_TAYGETE"},
    10090:{"ID":10090, "CENTER":521, "NAME":"IAU_CHALDENE"},
    10091:{"ID":10091, "CENTER":522, "NAME":"IAU_HARPALYKE"},
    10092:{"ID":10092, "CENTER":523, "NAME":"IAU_KALYKE"},
    10093:{"ID":10093, "CENTER":524, "NAME":"IAU_IOCASTE"},
    10094:{"ID":10094, "CENTER":525, "NAME":"IAU_ERINOME"},
    10095:{"ID":10095, "CENTER":526, "NAME":"IAU_ISONOE"},
    10096:{"ID":10096, "CENTER":527, "NAME":"IAU_PRAXIDIKE"},
    10097:{"ID":10097, "CENTER":1000005, "NAME":"IAU_BORRELLY"},
    10098:{"ID":10098, "CENTER":1000093, "NAME":"IAU_TEMPEL_1"},
    10099:{"ID":10099, "CENTER":2000004, "NAME":"IAU_VESTA"},
    10100:{"ID":10100, "CENTER":2025143, "NAME":"IAU_ITOKAWA"},
    13000:{"ID":13000, "CENTER":399, "NAME":"ITRF93"}}

# At load time, augment the PREDEFINED_FRAME_INFO to support lookups by name
# and by center ID as well as frame ID

for id in PREDEFINED_FRAME_INFO.keys():
    info = PREDEFINED_FRAME_INFO[id]
    PREDEFINED_FRAME_INFO[info["NAME"]] = info

    # The center of a frame can be used in multiple frames. Use only the first
    # for dictionary lookup
    try:
        info_by_center = PREDEFINED_FRAME_INFO[info["CENTER"]]

        # [center] maps to the centered frame with the smallest ID
        if info_by_center["ID"] > info["ID"]:
            PREDEFINED_FRAME_INFO[info["CENTER"]] = info

    except KeyError:
        PREDEFINED_FRAME_INFO[info["CENTER"]] = info

################################################################################
# BEGIN GRAMMAR
################################################################################
ParserElement.setDefaultWhitespaceChars(" ")

NEWLINE         = Suppress(Literal("\n"))

################################################################################
# An integer
################################################################################

SIGN            = oneOf("+ -")
UNSIGNED_INT    = Word(nums)
SIGNED_INT      = Combine(Optional(SIGN) + UNSIGNED_INT)
INT             = SIGNED_INT | UNSIGNED_INT

INTEGER         = Combine(Optional(SIGN) + UNSIGNED_INT)
INTEGER.setName("INTEGER")
INTEGER.setParseAction(lambda s,l,t: int(t[0]))

################################################################################
# A floating-point number
################################################################################

EXPONENT        = Suppress(oneOf("e E d D")) + INT
EXPONENT.setParseAction(lambda s,l,t:"e" + t[0])

FLOAT_WITH_INT  = Combine(INT
                        + "."
                        + Optional(UNSIGNED_INT)
                        + Optional(EXPONENT))
FLOAT_WO_INT    = Combine(Optional(SIGN)
                        + "."
                        + UNSIGNED_INT
                        + Optional(EXPONENT))
FLOAT_WO_DOT    = Combine(INT + EXPONENT)

FLOAT           = FLOAT_WITH_INT | FLOAT_WO_INT | FLOAT_WO_DOT
FLOAT.setName("FLOAT")
FLOAT.setParseAction(lambda s,l,t: float(t[0]))

################################################################################
# A character string
################################################################################

# This expression strips away the "'" characters surrounding a string, and also
# changes each internal "''" to a single "'". It does not handle continued
# strings; these are handled in the FromFile() instead.

QUOTEQUOTE      = Suppress(Literal("''"))
QUOTEQUOTE.setParseAction(lambda s, l, t: ["'"])

STRING          = (Suppress(Literal("'"))
                        + ZeroOrMore(CharsNotIn("'") | QUOTEQUOTE)
                        + Suppress(Literal("'")))
STRING.setName("STRING")
STRING.setParseAction(lambda s,l,t: "".join(t))

################################################################################
# A date-time is just an expression following "@" It is converted to a python
# datetime object. We note that a datetime object cannot express a leapsecond,
# but a leapsecond is unlikely to appear as a time in a SPICE text kernel.
################################################################################

DATE            = Combine(Suppress(Literal("@")) + CharsNotIn("@\n(), "))
DATE.setName("DATE")

########################################

def parse_datetime(s, l, tokens):
    """Converts a date expression to a Python datetime object, using the Julian
    Library's string parser."""

    try:
        (day, sec) = julian.day_sec_type_from_string(tokens[0],
                                                     validate=False)[0:2]
        # Validate=False is required to avoid an infinite recursion when reading
        # the leapseconds kernel, because the leapseconds kernel contains date
        # fields.
    except:
        raise ParseException("unrecognized time syntax: " + tokens[0])

    isec = int(sec)
    micro = int(1e6 * (sec - isec) + 0.5)

    return dt.datetime(2000,1,1) + dt.timedelta(day,isec,micro)
    # This will not handle leapseconds correctly, but a leapsecond is unlikely
    # to appear as a datetime in a SPICE text kenel.

DATE.setParseAction(parse_datetime)

################################################################################
# Values on the right side of an equal sign.
################################################################################

SCALAR          = FLOAT | INTEGER | STRING | DATE

LIST            = (Suppress(Literal("("))
                        + Suppress(ZeroOrMore(NEWLINE))
                        + OneOrMore(SCALAR
                        +   Suppress(ZeroOrMore(NEWLINE))
                        +   Suppress(Optional(","))
                        +   Suppress(ZeroOrMore(NEWLINE)))
                        + Suppress(Literal(")")))
LIST.setName("LIST")

def parse_list(s, l, tokens):
    """Interprets a list. A list containing a single item is converted to a
    scalar; anything else is converted to a Python list."""

    tokens = tokens.asList()

    # A single item in parentheses need not be a list
    if len(tokens) == 1: return tokens

    # Convert anything longer to a Python list
    return [tokens]

LIST.setParseAction(parse_list)

########################################
# UNIT TESTS
########################################

VALUE = SCALAR | LIST                     # order counts

class Test_VALUE(unittest.TestCase):

    def runTest(self):

        parser = VALUE + StringEnd()

        self.assertEqual(parser.parseString("  1234 ")[0],  1234)
        self.assertEqual(parser.parseString(" -1234 ")[0], -1234)
        self.assertEqual(parser.parseString(" +1234 ")[0],  1234)

        self.assertEqual(parser.parseString("  1234.      ")[0],  1234.)
        self.assertEqual(parser.parseString("  12340.e-01 ")[0],  1234.)
        self.assertEqual(parser.parseString("  12340e-1   ")[0],  1234.)
        self.assertEqual(parser.parseString("  234.5e+01  ")[0],  2345.)
        self.assertEqual(parser.parseString("  234.5D1    ")[0],  2345.)
        self.assertEqual(parser.parseString("  234.5d1    ")[0],  2345.)
        self.assertEqual(parser.parseString("  234.5E+001 ")[0],  2345.)
        self.assertEqual(parser.parseString(" +1234.      ")[0],  1234.)
        self.assertEqual(parser.parseString(" +12340.e-01 ")[0],  1234.)
        self.assertEqual(parser.parseString(" +12340e-1   ")[0],  1234.)
        self.assertEqual(parser.parseString(" +234.5e+01  ")[0],  2345.)
        self.assertEqual(parser.parseString(" +234.5D1    ")[0],  2345.)
        self.assertEqual(parser.parseString(" +234.5d1    ")[0],  2345.)
        self.assertEqual(parser.parseString(" +234.5E+001 ")[0],  2345.)
        self.assertEqual(parser.parseString(" -1234.0     ")[0], -1234.)
        self.assertEqual(parser.parseString(" -12340.e-01 ")[0], -1234.)
        self.assertEqual(parser.parseString(" -12340e-1   ")[0], -1234.)
        self.assertEqual(parser.parseString(" -234.5e+01  ")[0], -2345.)
        self.assertEqual(parser.parseString(" -234.5D1    ")[0], -2345.)
        self.assertEqual(parser.parseString(" -234.5d1    ")[0], -2345.)
        self.assertEqual(parser.parseString(" -234.5E+001 ")[0], -2345.)

        self.assertEqual(parser.parseString(" '  1234 '")[0], "  1234 ")
        self.assertEqual(parser.parseString("''' 1234 '")[0], "' 1234 ")
        self.assertEqual(parser.parseString("' 1234 '''")[0], " 1234 '")
        self.assertEqual(parser.parseString("' 12''34 '")[0], " 12'34 ")
        self.assertEqual(parser.parseString("''")[0],         "")
        self.assertEqual(parser.parseString("''''")[0],       "'")

        self.assertEqual(parser.parseString("@2001-Jan-01")[0],
            dt.datetime(2001,1,1))
        self.assertEqual(parser.parseString("@2001-Jan-01:12:34:56.789")[0],
            dt.datetime(2001,1,1,12,34,56,789000))

        self.assertEqual(parser.parseString("(1,2,3)")[0],    [1,2,3])
        self.assertEqual(parser.parseString("(1)")[0],        1)
        self.assertEqual(parser.parseString("(1,2, \n3)")[0], [1,2,3])
        self.assertEqual(parser.parseString("('1','2')")[0],  ["1","2"])
        self.assertEqual(parser.parseString("('1''','2')")[0],["1'","2"])
        self.assertEqual(parser.parseString("(1, @Jul-4-1776)")[0],
            [1, dt.datetime(1776,7,4)])

        # Doesn't recognize...
        self.assertRaises(ParseException, parser.parseString, "  1234 .  ")
        self.assertRaises(ParseException, parser.parseString, "- 12340e-1")
        self.assertRaises(ParseException, parser.parseString, "-12340 e-1")
        self.assertRaises(ParseException, parser.parseString, "-12340e -1")
        self.assertRaises(ParseException, parser.parseString, "-12340e- 1")

        self.assertRaises(ParseException, parser.parseString, "@ 2001-Jan-01")
        self.assertRaises(ParseException, parser.parseString, "@2001 -Jan-01")
        self.assertRaises(ParseException, parser.parseString, "@2001- Jan-01")

        # A tab character is not supposed to be treated as whitespace
        # self.assertRaises(ParseException, parser.parseString, "\t1")
        # self.assertRaises(ParseException, parser.parseString, "1\t")

################################################################################
# Expressions are of the form name = value or name += value. They can include
# embedded newlines.
################################################################################

DEFINITION      = (Suppress(ZeroOrMore(NEWLINE))
                        + Literal("=")
                        + Suppress(ZeroOrMore(NEWLINE))
                        + VALUE
                        + Suppress(OneOrMore(NEWLINE)))
DEFINITION.setName("DEFINITION")

EXPRESSION      = (Suppress(ZeroOrMore(NEWLINE))
                        + oneOf("= +=")
                        + Suppress(ZeroOrMore(NEWLINE))
                        + VALUE
                        + Suppress(OneOrMore(NEWLINE)))
EXPRESSION.setName("EXPRESSION")

################################################################################
# A simple parameter name contains no digits or slashes
################################################################################

complex_chars   = " .(),=\t\n\r/0123456789-+"
SIMPLE_PARAM    = Combine(CharsNotIn(complex_chars))

SIMPLE_EXPR     = SIMPLE_PARAM + EXPRESSION
SIMPLE_EXPR.setName("SIMPLE_EXPR")

########################################

def apply_simple_expr(s, l, tokens, dict=DICTIONARY):
    """Adds or appends a new entry to the given dictionary. It also concatenates
    strings as appropriate."""

    name  = tokens[0]
    op    = tokens[1]
    value = tokens[2]

    # If it's a definition, insert into the dictionary
    if op == "=":
        dict[name] = value
        apply_concatenation(dict, name, 0)
        return

    # If it is not already in the dictionary, add it to the dictionary now
    try:
        current = dict[name]
    except KeyError:
        dict[name] = value
        apply_concatenation(dict, name, 0)
        return

    # Convert the current value to a list if necessary
    if type(current) != type([]):
        dict[name] = [current]

    # Append the new list
    nvalues = len(dict[name])
    if type(value) == type([]):
        dict[name] += value
    else:
        dict[name] += [value]

    # Handle string concatenation operators "//"
    apply_concatenation(dict, name, nvalues-1)

    # Convert it back to a string if appropriate
    if len(dict[name]) == 1: dict[name] = dict[name][0]

########################################

def apply_concatenation(dict, name, index):
    """This method concatenates strings when two appear together in a list and
    the first ends in "//" plus optional whitespace"""

    # Get the current value
    value = dict[name]

    # If it is not a list, return
    if type(value) != type([]): return

    # Initialize the result list
    result = value[:index]
    value = value[index:]

    # Iterate through consecutive pairs of list elements
    while (len(value) > 1):
        try:
            # The next two items must be strings
            if type(value[0]) != type(""): raise ValueError
            if type(value[1]) != type(""): raise ValueError

            # The first string must end with "//" + whitespace
            trimmed = value[0].rstrip()
            if not trimmed.endswith("//"): raise ValueError

            # Concatenate and continue
            merged = trimmed[:-2] + value[1]
            value = [merged] + value[2:]

        # Otherwise, move the first item to the result list and continue
        except ValueError:
            result.append(value[0])
            value = value[1:]

    # Just copy the last item when the list length reaches one
    result += value

    # Update the dictionary
    dict[name] = result

SIMPLE_EXPR.setParseAction(apply_simple_expr)

################################################################################
# A general parameter name is any remaining name compatible with the syntax
################################################################################

excluded_chars  = " .(),=\t\n\r"
GENERAL_PARAM   = Combine(CharsNotIn(excluded_chars))

GENERAL_EXPR    = GENERAL_PARAM + EXPRESSION
GENERAL_EXPR.setName("GENERAL_EXPR")

# This method adds a new entry to the given dictionary
GENERAL_EXPR.setParseAction(apply_simple_expr)

################################################################################
# A prefixed parameter has a prefix and a slash, followed by another parameter
# name. The prefix indexes the top-level dictionary, returning a dictionary of
# the subsequent parameter names. Example:
#       DELTET/DELTA_T_A = 32.184
# An prefixed parameter is entered into the dictionary as a leading dictionary
# keyed by the prefix, returning a sub-dictionary of the specified parameters.
################################################################################

PREFIXED_EXPR   = (OneOrMore(SIMPLE_PARAM + Suppress(Literal("/")))
                        + SIMPLE_PARAM + EXPRESSION)
PREFIXED_EXPR.setName("PREFIXED_EXPR")

########################################

def get_prefixed_subdict(token, dict):
    """Returns the sub-dictionary of the given dictionary, creating an empty one
    if necessary."""

    # Example: DELTET/DELTA_T_A = 32.184

    # Look up or create the DELTET sub-dictionary
    try:
        subdict = dict[token]
        if type(subdict) == type({}):
            return dict[token]
    except KeyError:
        pass

    dict[token] = {}
    return dict[token]

########################################

def apply_prefixed_expr(s, l, tokens, dict=DICTIONARY):
    """Adds a new prefixed item to the dictionary, creating the sub-dictionary
    if necessary."""

    # Example: DELTET/DELTA_T_A = 32.184

    # Find or create the dict["DELTET"] sub-dictionary, recursively
    subdict = dict
    for i in range(len(tokens)-3):
        subdict = get_prefixed_subdict(tokens[i], subdict)

    # Pass the remaining tokens on recursively
    apply_simple_expr(s, l, tokens[-3:], subdict)

PREFIXED_EXPR.setParseAction(apply_prefixed_expr)

################################################################################
# An indexed parameter name contains a prefix string followed by a positive or
# negative integer, followed by a suffix string. Examples:
#       BODY399_POLE_RA
#       FRAME_624_NAME
# An indexed parameter is entered into the dictionary as a leading dictionary
# keyed by the prefix, a sub-dictionary keyed by the index, and a
# sub-sub-dictionary keyed by the suffix. Underscores surrounding the integer
# are suppressed.
#
# Only specific prefixes are identified for indexing. They are BODY, FRAME,
# TKFRAME, TKFRAME_DSS, INS, CK, SCLK.
#
# Whenever the suffix string is "NAME", the name is entered into the
# prefix dictionary so that [name] and [index] point to the same information.
#
# Whenever a BODY is created with a new index, any pre-defined names are also
# entered into the prefix dictionary.
#
# Whenever a new FRAME is created with a new index, any pre-defined name or
# center body is also entered into the prefix dictionary.
################################################################################

INDEXED_EXPR    = (oneOf("BODY_ BODY FRAME_ FRAME SCLK_ SCLK " +
                         "TKFRAME_ TKFRAME TKFRAME_DSS INS CK CK_")
                        + INTEGER
                        + Suppress(Literal("_"))
                        + GENERAL_PARAM
                        + EXPRESSION)
INDEXED_EXPR.setName("INDEXED_EXPR")

########################################

def get_indexed_dict(tokens, dict=DICTIONARY):
    """Returns the needed sub-sub-dictionary identified by a numeric index,
    creating an empty one if necessary."""

    # Example: BODY699_RADII = (60330. 60330. 60330.)

    # Suppress a trailing underscore before the index
    prefix = tokens[0]
    if prefix[-1] == "_": prefix = prefix[:-1]

    id = tokens[1]
    suffix = tokens[2]
    value = tokens[4]

    # Lookup or create the [prefix] sub-dictionary
    try:
        subdict = dict[prefix]
    except KeyError:
        subdict = {}
        dict[prefix] = subdict

    # Lookup or create the [index] sub-sub-dictionary
    try:
        subsubdict = subdict[id]
    except KeyError:
        subsubdict = {}
        subdict[id] = subsubdict

        # And index sub-sub-dictionary always has an entry "ID"
        subsubdict["ID"] = id

        # If this is a new sub-dictionary for a pre-defined body, then let
        # BODY[name] point to the same sub-sub-dictionary

        if prefix == "BODY":
            try:
                name = PREDEFINED_BODY_NAME_FROM_ID[id]

                # A body can have multiple names, so search the name list
                for name in PREDEFINED_BODY_ID_FROM_NAME.keys():
                    if PREDEFINED_BODY_ID_FROM_NAME[name] == id:
                        subdict[name] = subsubdict

            except KeyError: pass

        # If this is a new sub-dictionary for a pre-defined frame, then let
        # FRAME[name] and FRAME[center] point to the same sub-sub-dictionary

        if prefix == "FRAME":
            try:
                info = PREDEFINED_FRAME_INFO[id]
                subsubdict["NAME"] = info["NAME"]
                subdict[info["NAME"]] = subsubdict

                subsubdict["ID"] = info["ID"]
                subdict[info["ID"]] = subsubdict

                subsubdict["CENTER"] = info["CENTER"]

                # A body can be at the center of multiple frames, so don't
                # overwrite something already there
                try:
                    test = subdict[info["CENTER"]]
                except KeyError:
                    subdict[info["CENTER"]] = subsubdict

            except KeyError: pass

    # If this is a name, add a new pointer to the dictionary
    if suffix == "NAME":
        subdict[value] = subsubdict

    # If this is the center of a new frame, add a new pointer to the dictionary
    if prefix == "FRAME" and suffix == "CENTER":
        try:
            test = subdict[value]
        except KeyError:
            subdict[value] = subsubdict

    # If this is the FOV_FRAME of a new INS, add a new pointer to the dictionary
    if prefix == "INS" and suffix == "FOV_FRAME":
        try:
            test = subdict[value]
        except KeyError:
            subdict[value] = subsubdict

    return subsubdict

########################################

def apply_indexed_expr(s, l, tokens, dict=DICTIONARY):
    """Inserts a definition into an indexed dictionary."""

    # Example: BODY699_RADII = (60330. 60330. 60330.)

    # Find or create dict["BODY"][699] dictionary
    subsubdict = get_indexed_dict(tokens, dict)

    # Define RADII in the sub-sub-dictionary
    apply_simple_expr(s, l, tokens[2:], dict=subsubdict)

INDEXED_EXPR.setParseAction(apply_indexed_expr)

################################################################################
# A NAIF_BODY parameter associates a body ID and its name. Example:
#       NAIF_BODY_CODE       += ( 644 )
#       NAIF_BODY_NAME       += ( 'HYROKKIN' )
# When NAIF_BODY_NAME and NAIF_BODY_CODE are both defined, the corresponding
# subdictionaries dict["BODY"][code] and dict["BODY"][name] become equivalent.
################################################################################

NAIF_BODY_CODE_EXPR = Literal("NAIF_BODY_CODE") + EXPRESSION
NAIF_BODY_NAME_EXPR = Literal("NAIF_BODY_NAME") + EXPRESSION
NAIF_BODY_CODE_EXPR.setName("NAIF_BODY_CODE_EXPR")
NAIF_BODY_NAME_EXPR.setName("NAIF_BODY_NAME_EXPR")

########################################

def link_body_dictionaries(dict, arg1, arg2):
    """This method links BODY dictionaries indexed by name and numeric ID."""

    # Get the current list
    list1 = dict[arg1]
    if type(list1) != type([]): list1 = [list1]

    # Make sure a "BODY" dictionary exists
    try:
        body_dict = dict["BODY"]
    except KeyError:
        body_dict = {}
        dict["BODY"] = body_dict

    # Get the second list; create it if necessary
    try:
        list2 = dict[arg2]
        if type(list2) != type([]): list2 = [list2]
    except KeyError:
        list2 = []
        dict[arg2] = list2

    # Link the dictionaries if possible
    if len(list1) == len(list2):
        body_dict[list1[-1]] = body_dict[list2[-1]]

        # ... and then insert "NAME" and "ID" entries
        if type(list1[-1]) == type(0):
            body_dict[list1[-1]]["ID"] = list1[-1]
            body_dict[list1[-1]]["NAME"] = list2[-1]
        else:
            body_dict[list1[-1]]["ID"] = list2[-1]
            body_dict[list1[-1]]["NAME"] = list1[-1]

    # Otherwise, create an empty dictionary
    else:
        body_dict[list1[-1]] = {}

def apply_naif_body_code_expr(s, l, tokens, dict=DICTIONARY):
    apply_simple_expr(s, l, tokens, dict=DICTIONARY)
    link_body_dictionaries(dict, "NAIF_BODY_CODE", "NAIF_BODY_NAME")

def apply_naif_body_name_expr(s, l, tokens, dict=DICTIONARY):
    apply_simple_expr(s, l, tokens, dict=DICTIONARY)
    link_body_dictionaries(dict, "NAIF_BODY_NAME", "NAIF_BODY_CODE")

NAIF_BODY_CODE_EXPR.setParseAction(apply_naif_body_code_expr)
NAIF_BODY_NAME_EXPR.setParseAction(apply_naif_body_name_expr)

################################################################################
# Putting the pieces together...
################################################################################

STATEMENT       = (NAIF_BODY_CODE_EXPR | NAIF_BODY_NAME_EXPR |
                   PREFIXED_EXPR | INDEXED_EXPR | GENERAL_EXPR)

TEXT_KERNEL     = OneOrMore(ZeroOrMore(NEWLINE) + STATEMENT) + StringEnd()

########################################
# UNIT TESTS
########################################

class Test_STATEMENT(unittest.TestCase):

    def runTest(self):

        DICTIONARY.clear()
        parser = STATEMENT + StringEnd()

        # Tests of simple definitions and augmentations
        parser.parseString(" A = 1 \n")
        self.assertEqual(DICTIONARY["A"], 1)

        parser.parseString(" A = 2 \n")
        self.assertEqual(DICTIONARY["A"], 2)

        parser.parseString(" A += 3 \n")
        self.assertEqual(DICTIONARY["A"], [2,3])

        parser.parseString(" B += 4 \n")
        self.assertEqual(DICTIONARY["B"], 4)

        # Tests of expanding lists
        parser.parseString("D = (1.)\n")
        self.assertEqual(DICTIONARY["D"], 1.)
        parser.parseString("D += 2.\n")
        self.assertEqual(DICTIONARY["D"], [1.,2.])

        parser.parseString("D = 3.\n")
        parser.parseString("D += 4.\n")
        self.assertEqual(DICTIONARY["D"], [3.,4.])

        parser.parseString("D = 5.\n")
        parser.parseString("D += (6.)\n")
        self.assertEqual(DICTIONARY["D"], [5.,6.])

        parser.parseString("D = (7.)\n")
        parser.parseString("D += (8.)\n")
        self.assertEqual(DICTIONARY["D"], [7.,8.])

        parser.parseString("D = (9.,10.)\n")
        self.assertEqual(DICTIONARY["D"], [9.,10.])
        parser.parseString("D += 11.\n")
        self.assertEqual(DICTIONARY["D"], [9.,10.,11.])
        parser.parseString("D += (12.)\n")
        self.assertEqual(DICTIONARY["D"], [9.,10.,11.,12.])
        parser.parseString("D += (13.,14.)\n")
        self.assertEqual(DICTIONARY["D"], [9.,10.,11.,12.,13.,14.])

        # Tests of string concatenation
        parser.parseString("E = ('Antidis// ','establish// ','mentarianism')\n")
        self.assertEqual(DICTIONARY["E"], ["Antidisestablishmentarianism"])

        parser.parseString("E = 'T''was brillig and //  '\n")
        parser.parseString("E += 'the slithy toves'\n")
        self.assertEqual(DICTIONARY["E"], "T'was brillig and the slithy toves")

        parser.parseString("E += 'Did gyre and //  '\n")
        parser.parseString("E += 'gimble in the wabe'  \n")
        self.assertEqual(DICTIONARY["E"], ["T'was brillig and the slithy toves",
                                           "Did gyre and gimble in the wabe"])

        parser.parseString("F += 'Four score //  '\n")
        parser.parseString("F += '//'  \n")
        parser.parseString("F += 'and seven //'  \n")
        self.assertEqual(DICTIONARY["F"], "Four score and seven //")

        parser.parseString("F += ('years //  ')  \n")
        self.assertEqual(DICTIONARY["F"], "Four score and seven years //  ")

        parser.parseString("F += ('ago','our fathers //', 'brought forth')\n")
        self.assertEqual(DICTIONARY["F"], ["Four score and seven years ago",
                                           "our fathers brought forth"])

        # Tests of prefixed definitions and augmentations
        parser.parseString(" B/C = 5 \n")
        self.assertEqual(DICTIONARY["B"]["C"], 5)

        parser.parseString(" B/C/D = 6 \n")
        self.assertEqual(DICTIONARY["B"]["C"]["D"], 6)

        parser.parseString(" B/C/D += 7 \n")
        self.assertEqual(DICTIONARY["B"]["C"]["D"], [6,7])

        parser.parseString(" B/C/D += (8) \n")
        self.assertEqual(DICTIONARY["B"]["C"]["D"], [6,7,8])

        parser.parseString(" B/C/D += (9,10,11)\n")
        self.assertEqual(DICTIONARY["B"]["C"]["D"], [6,7,8,9,10,11])

        # Tests of BODY codes and names
        parser.parseString(" NAIF_BODY_CODE += ( 698 )\n")
        parser.parseString(" NAIF_BODY_NAME += ( 'TEST' )\n")
        self.assertEqual(DICTIONARY["BODY"][698], DICTIONARY["BODY"]["TEST"])
        self.assertEqual(DICTIONARY["BODY"][698]["ID"], 698)
        self.assertEqual(DICTIONARY["BODY"][698]["NAME"], "TEST")

        parser.parseString(" BODY698_RADII = (100., 90., 80.)\n")
        self.assertEqual(DICTIONARY["BODY"][698]["RADII"][2], 80.)
        self.assertEqual(DICTIONARY["BODY"][698], DICTIONARY["BODY"]["TEST"])

        parser.parseString("BODY699_RADII = (60330.)\n")
        self.assertEqual(DICTIONARY["BODY"][699]["RADII"], 60330.)
        self.assertEqual(DICTIONARY["BODY"]["SATURN"]["RADII"], 60330.)

        # Tests of FRAME codes, names and centers
        parser.parseString("FRAME_1698_NAME = 'IAU_TEST'\n")
        self.assertEqual(DICTIONARY["FRAME"][1698]["NAME"], "IAU_TEST")
        self.assertEqual(DICTIONARY["FRAME"][1698]["ID"], 1698)
        self.assertEqual(DICTIONARY["FRAME"][1698],
                         DICTIONARY["FRAME"]["IAU_TEST"])

        parser.parseString("FRAME_1698_CENTER = 698\n")
        self.assertEqual(DICTIONARY["FRAME"][698], DICTIONARY["FRAME"][1698])

        parser.parseString("FRAME_1697_NAME = 'INERTIAL'\n")
        self.assertEqual(DICTIONARY["FRAME"][1697]["NAME"], "INERTIAL")
        self.assertEqual(DICTIONARY["FRAME"][1697]["ID"], 1697)
        self.assertEqual(DICTIONARY["FRAME"][1697],
                         DICTIONARY["FRAME"]["INERTIAL"])

        parser.parseString("FRAME_1697_CENTER = 698\n")
        self.assertEqual(DICTIONARY["FRAME"][698], DICTIONARY["FRAME"][1698])

        parser.parseString("FRAME_618_CLASS =  2 \n")
        self.assertEqual(DICTIONARY["FRAME"][618]["CLASS"], 2)
        self.assertEqual(DICTIONARY["FRAME"]["IAU_PAN"]["CLASS"], 2)
        self.assertEqual(DICTIONARY["FRAME"]["IAU_PAN"]["NAME"], "IAU_PAN")
        self.assertEqual(DICTIONARY["FRAME"]["IAU_PAN"]["CENTER"], 618)
        self.assertEqual(DICTIONARY["FRAME"]["IAU_PAN"]["ID"], 10082)
        self.assertEqual(DICTIONARY["FRAME"][618], DICTIONARY["FRAME"][10082])

        # Tests of general names
        parser.parseString("FRAME_IAU_S7_2004 = 65035\n")
        self.assertEqual(DICTIONARY["FRAME_IAU_S7_2004"], 65035)

################################################################################
# Parsing methods
################################################################################

def ParseText(kernel_text, commented=False, clear=True):
    """This routine parses a string as a text kernel, returning a dictionary of
    the values found.

    Input:
        kernel_text     the contents os a SPICE text kernel. It can be
                        represented as a string, with newlines between the
                        lines, or as a list of strings.

        commented       True if the kernel text contains comments delimited by
                        \\begintext and \\begindata; False otherwise. Default is
                        False.

        clear           True to erase the contents of the dictionary returned by
                        a prior call to ParseText(); False to merge the contents
                        of the new dictionary with the previous one.

    Return:             A dictionary containing all the parameters in the given
                        SPICE text kernel.

    Note that the returned dictionary is keyed in a very specific way based on
    the structure of the keyword names in the kernel. Examples:
        BODY399_POLE_RA     dict["BODY"][399]["POLE_RA"]
        MESSAGE             dict["MESSAGE"]
        DELTET/EB           dict["DELTET"]["EB"]
        FRAME_624_NAME      dict["FRAME"][624]["NAME"]

    Also, frames and bodies can be referenced by their name or their numeric ID.
    These are equivalent:
        dict["FRAME"][623]      dict["FRAME"]["IAU_SUTTUNGR"]
        dict["BODY"][399]       dict["BODY"]["SATURN"]
    """

    # Clear the dictionary if necessary
    if clear: DICTIONARY.clear()

    # Strip the comments if necessary
    if commented:

        # Convert to a list of strings separated by newlines
        if type(kernel_text) == type(""): kernel_text = kernel.split("\n")

        # Filter out the the comment lines
        is_data = False
        filtered = []
        for line in kernel_text:
            stripped = line.strip()
            if stripped == "\\begindata":
                is_data = True
            elif stripped == "\\begintext":
                is_data = False
            elif is_data and line.strip() != "":
                filtered.append(stripped)

        kernel_text = filtered

    # Convert to a single string with embedded newlines
    if type(kernel_text) == type([]):
        kernel_text = "\n".join(kernel_text) + "\n"

    # Parse the string
    ignore = TEXT_KERNEL.parseString(kernel_text)

    # Return the dictionary
    return DICTIONARY.copy()

########################################

def FromFile(filename, clear=True):
    """This routine reads a text kernel returning a dictionary of the values
    found.

    Input:
        filename        the file path and name of a text kernel file.

        clear           True to erase the contents of the dictionary returned by
                        a prior call to ParseText(); False to merge the contents
                        of the new dictionary with the previous one.

    Return:             A dictionary containing all the parameters in the given
                        SPICE text kernel.

    Note that the returned dictionary is keyed in a very specific way based on
    the structure of the keyword names in the kernel. Examples:
        BODY399_POLE_RA     dict["BODY"][399]["POLE_RA"]
        MESSAGE             dict["MESSAGE"]
        DELTET/EB           dict["DELTET"]["EB"]
        FRAME_624_NAME      dict["FRAME"][624]["NAME"]

    Also, frames and bodies can be referenced by their name or their numeric ID.
    These are equivalent:
        dict["FRAME"][623]      dict["FRAME"]["IAU_SUTTUNGR"]
        dict["BODY"][399]       dict["BODY"]["SATURN"]

    Frame and body dictionaries also have keywords "ID" and "NAME" added if the
    name is available. These make it easy to get the ID of something given its
    name, or vice-versa. Example:
        dict["FRAME"]["IAU_SUTTUNGR"]["ID"] = 623
        dict["FRAME"][623]["ID"] = 623
        dict["FRAME"][623]["NAME"] = IAU_SUTTUNGR
    """

    # Open the file
    f = open(filename)

    # Create a list of lines
    kernel_text = f.readlines()

    # Close the file
    f.close()

    # Parse the string and return the dictionary
    return ParseText(kernel_text, commented=True, clear=clear)

########################################

def DefaultBodies(clear=True):
    """This routine loads a dictionary with all of the default body information.

    Input:
        clear           True to erase the contents of the dictionary returned by
                        a prior call to ParseText(); False to merge the contents
                        of the new dictionary with the previous one.

    Return:             A dictionary containing all the default body
                        information.
    """

    if clear: DICTIONARY.clear()

    # Get the BODY dictionary, creating one if necessary
    try:
        bodydict = DICTIONARY["BODY"]
    except KeyError:
        bodydict = {}
        DICTIONARY["BODY"] = bodydict

    # Look up each pre-defined id and add the dictionary if necessary
    for id in PREDEFINED_BODY_NAME_FROM_ID.keys():
        try:
            dict_by_id = bodydict[id]
        except KeyError:
            dict_by_id = {"ID":id, "NAME":PREDEFINED_BODY_NAME_FROM_ID[id]}
            bodydict[id] = dict_by_id

    # Look up each pre-defined name and create a dictionary that points to the
    # corresponding dictionary (which already exists now)
    for name in PREDEFINED_BODY_ID_FROM_NAME.keys():
        try:
            dict_by_name = bodydict[name]
        except KeyError:
            bodydict[name] = bodydict[PREDEFINED_BODY_ID_FROM_NAME[name]]

    return DICTIONARY

########################################

def DefaultFrames(clear=True):
    """This routine loads a dictionary with all of the default frame
    information.

    Input:
        clear           True to erase the contents of the dictionary returned by
                        a prior call to ParseText(); False to merge the contents
                        of the new dictionary with the previous one.

    Return:             A dictionary containing all the default body
                        information.
    """

    if clear: DICTIONARY.clear()

    # Get the FRAME dictionary, creating one if necessary
    try:
        framedict = DICTIONARY["FRAME"]
    except KeyError:
        framedict = {}
        DICTIONARY["FRAME"] = framedict

    # Look up each pre-defined frame and add it to the dictionary if necessary
    for info in PREDEFINED_FRAME_INFO.values():

        # Find the info by name
        try:
            info_by_name = framedict[info["NAME"]]
        except KeyError:
            info_by_name = {"ID":info["ID"], "NAME":info["NAME"],
                            "CENTER":info["CENTER"]}
            framedict[info["NAME"]] = info_by_name

        # Point to it by ID if necessary
        try:
            test = framedict[info["ID"]]
        except KeyError:
            framedict[info["ID"]] = framedict[info["NAME"]]

    # Look up each pre-defined center body and add it to the dictionary if
    # necessary. This is a separate loop to ensure that the center body maps
    # to the same frame as it does in the pre-defined dictionary.

    for info in PREDEFINED_FRAME_INFO.values():
        center = info["CENTER"]
        try:
            test = framedict[center]
        except KeyError:
            framedict[center] = framedict[PREDEFINED_FRAME_INFO[center]["NAME"]]

    return DICTIONARY

########################################
# UNIT TESTS
########################################

class Test_FromFile(unittest.TestCase):

  def runTest(self):

    # Test DefaultBodies()
    dict = DefaultBodies(clear=True)
    self.assertEqual(dict["BODY"][618], dict["BODY"]["PAN"])
    self.assertEqual(dict["BODY"][618]["NAME"], "PAN")
    self.assertEqual(dict["BODY"][618]["ID"],     618)

    # ... make sure it does not replace a pre-existing definition
    DICTIONARY.clear()
    DICTIONARY["BODY"] = {618: {"ID":618, "NAME":"ALIAS"}}
    DICTIONARY["BODY"]["ALIAS"] = DICTIONARY["BODY"][618]

    dict = DefaultBodies(clear=False)

    self.assertEqual(dict["BODY"][618],   dict["BODY"]["ALIAS"])
    self.assertEqual(dict["BODY"]["PAN"], dict["BODY"]["ALIAS"])
    self.assertEqual(dict["BODY"]["PAN"]["NAME"], "ALIAS")
    self.assertEqual(dict["BODY"]["PAN"]["ID"],      618)

    # Test DefaultFrames()
    dict = DefaultFrames(clear=True)
    self.assertEqual(dict["FRAME"][618], dict["FRAME"]["IAU_PAN"])
    self.assertEqual(dict["FRAME"][618], dict["FRAME"][10082])
    self.assertEqual(dict["FRAME"][618]["ID"],       10082)
    self.assertEqual(dict["FRAME"][618]["NAME"], "IAU_PAN")
    self.assertEqual(dict["FRAME"][618]["CENTER"],     618)

    self.assertEqual(dict["FRAME"][399]["NAME"], "IAU_EARTH")
    self.assertEqual(dict["FRAME"]["IAU_EARTH"]["CENTER"], 399)
    self.assertEqual(dict["FRAME"]["ITRF93"]["CENTER"],    399)

    # ... make sure it does not replace a pre-existing definition
    DICTIONARY.clear()
    DICTIONARY["FRAME"] = {618: {"CENTER":618, "NAME":"NOT_IAU", "ID":11111}}

    dict = DefaultFrames(clear=False)

    self.assertEqual(dict["FRAME"][10082], dict["FRAME"]["IAU_PAN"])
    self.assertEqual(dict["FRAME"][10082]["ID"],       10082)
    self.assertEqual(dict["FRAME"][10082]["NAME"], "IAU_PAN")
    self.assertEqual(dict["FRAME"][10082]["CENTER"],     618)

    self.assertEqual(dict["FRAME"][618]["ID"],       11111)
    self.assertEqual(dict["FRAME"][618]["NAME"], "NOT_IAU")
    self.assertEqual(dict["FRAME"][618]["CENTER"],     618)

    # Test FromFile() by attempting to parse every text kernel
    prefix = "/Library/WebServer/SPICE/"
    filenames = ["Cassini/FK/cas_rocks_v18.tf",
                 "Cassini/FK/cas_status_v04.tf",
                 "Cassini/FK/cas_v40.tf",
                 "Cassini/FK/earth_topo_050714.tf",
                 "Cassini/IK/cas_caps_v03.ti",
                 "Cassini/IK/cas_cda_v01.ti",
                 "Cassini/IK/cas_cirs_v09.ti",
                 "Cassini/IK/cas_inms_v02.ti",
                 "Cassini/IK/cas_iss_v10.ti",
                 "Cassini/IK/cas_mag_v01.ti",
                 "Cassini/IK/cas_mimi_v11.ti",
                 "Cassini/IK/cas_radar_v11.ti",
                 "Cassini/IK/cas_rpws_v01.ti",
                 "Cassini/IK/cas_rss_v03.ti",
                 "Cassini/IK/cas_sru_v02.ti",
                 "Cassini/IK/cas_uvis_v06.ti",
                 "Cassini/IK/cas_vims_v06.ti",
                 "Cassini/PCK/cpck07Jan2010.tpc",
                 "Cassini/PCK/cpck09Mar2011.tpc",
                 "Cassini/PCK/cpck09Mar2011_Nav.tpc",
                 "Cassini/PCK/cpck14Oct2010.tpc",
                 "Cassini/PCK/cpck14Oct2010_Nav.tpc",
                 "Cassini/PCK/cpck16Jun2010.tpc",
                 "Cassini/PCK/cpck16Jun2010_Nav.tpc",
                 "Cassini/PCK/cpck_rock_11May2009_merged.tpc",
                 "Cassini/PCK/cpck_rock_21Jan2011.tpc",
                 "Cassini/PCK/cpck_rock_21Jan2011_merged.tpc",
                 "Cassini/SCLK/cas00136.tsc",
                 "Cassini/SCLK/cas00144.tsc",
                 "Cassini/SCLK/cas00145.tsc",
                 "Cassini/SCLK/cas00147.tsc",
                 "Galileo/PCK/mips_010314.tpc",
                 "Galileo/PCK/pck00007.tpc",
                 "Galileo/PCK/pk96030a.tpc",
                 "Galileo/SCLK/mk00062a.tsc",
                 "General/LSK/naif0009.tls",
                 "General/PCK/pck00008.tpc",
                 "General/PCK/pck00008_edit.tpc",
                 "General/PCK/pck00009.tpc",
                 "Juno/IK/juno_jade_v00.ti",
                 "Juno/IK/juno_jedi_v00.ti",
                 "Juno/IK/juno_jiram_v00.ti",
                 "Juno/IK/juno_junocam_v00.ti",
                 "Juno/IK/juno_mag_v00.ti",
                 "Juno/IK/juno_mwr_v00.ti",
                 "Juno/IK/juno_struct_v00.ti",
                 "Juno/IK/juno_uvs_v00.ti",
                 "Juno/IK/juno_waves_v00.ti",
                 "Juno/SCLK/JNO_SCLKSCET.00000.tsc",
                 "Juno/SPK/juno_v02.tf",
                 "Mars/PCK/mars_iau2000_v0.tpc",
                 "New-Horizons/FK/nh_v110.tf",
                 "New-Horizons/IK/nh_alice_v101.ti",
                 "New-Horizons/IK/nh_lorri_v100.ti",
                 "New-Horizons/IK/nh_pepssi_v110.ti",
                 "New-Horizons/IK/nh_ralph_v100.ti",
                 "New-Horizons/IK/nh_rex_v100.ti",
                 "New-Horizons/IK/nh_sdc_v100.ti",
                 "New-Horizons/IK/nh_swap_v100.ti",
                 "New-Horizons/SCLK/new_horizons_295.tsc",
                 "Saturn/FK/cas_rocks_v10.tf",
                 "Saturn/PCK/cassini_merged.tpc",
                 "Saturn/PCK/cpck30Jul2007.tpc",
                 "Saturn/PCK/cpck30Jul2007_Nav.tpc",
                 "Saturn/PCK/cpck_rock_19Apr2007_merged.tpc",
                 "Voyager/FK/vg1_v02.tf",
                 "Voyager/FK/vg2_v02.tf",
                 "Voyager/IK/vg1_issna_v02.ti",
                 "Voyager/IK/vg1_isswa_v01.ti",
                 "Voyager/IK/vg2_issna_v02.ti",
                 "Voyager/IK/vg2_isswa_v01.ti",
                 "Voyager/SCLK/vg100010.tsc",
                 "Voyager/SCLK/vg100011.tsc",
                 "Voyager/SCLK/vg200010.tsc",
                 "Voyager/SCLK/vg200011.tsc"]

    for file in filenames:
        print file
        d = FromFile(prefix + file)
        #print d
        #print "*******************************"

################################################################################
# Perform unit testing if executed from the command line
################################################################################

if __name__ == "__main__":
    unittest.main()

################################################################################
