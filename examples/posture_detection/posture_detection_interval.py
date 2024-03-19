from ifis.interval_fuzzy_sets import *
from ifis.interval_fuzzy_system import *
from ifis.interval_linguistic_variable import *

import fuzzyfication as fz
from examples.posture_detection.import_data import *

# reading data
data_dict1 = ImportData.read_raw_data_pickle_file("data/features2D.pickle", False, 'HeightWidthRatio')
data_dict2 = ImportData.read_raw_data_pickle_file("data/features3D.pickle", False, "P40", "HHmaxRatio",
                                                  "MaxStdXZ")
data_dict3 = ImportData.read_raw_data_pickle_file("data/classes.pickle", False, "class")

data_array = ImportData.convert_data_dict2table(data_dict2[1], data_dict1[1], data_dict3[1])

FS = IntervalFuzzySystem(type_system=2)

F_HW_low = IntervalFuzzySet(function_start=fz.fun_HW_low, term="low")
F_HW_med = IntervalFuzzySet(function_start=fz.fun_HW_med, term="medium")
F_HW_high = IntervalFuzzySet(function_start=fz.fun_HW_high, term="high")
lv_in1 = IntervalLinguisticVariable([F_HW_low, F_HW_med, F_HW_high], concept="HW", universe_of_discourse=[0, 4])
lv_in1.plot()
FS.add_linguistic_variable("HW", lv_in1)

F_HHmax_low = IntervalFuzzySet(function_start=fz.fun_HHmax_low, term="low")
F_HHmax_med = IntervalFuzzySet(function_start=fz.fun_HHmax_med, term="medium")
F_HHmax_high = IntervalFuzzySet(function_start=fz.fun_HHmax_high, term="high")
lv_in2 = IntervalLinguisticVariable([F_HHmax_low, F_HHmax_med, F_HHmax_high], concept="HHmax",
                                    universe_of_discourse=[0, 1.5])
lv_in2.plot()
FS.add_linguistic_variable("HHmax", lv_in2)

F_sigma_low = IntervalFuzzySet(function_start=fz.fun_sigma_low, term="low")
F_sigma_med = IntervalFuzzySet(function_start=fz.fun_sigma_med, term="medium")
F_sigma_high = IntervalFuzzySet(function_start=fz.fun_sigma_high, term="high")
lv_in3 = IntervalLinguisticVariable([F_sigma_low, F_sigma_med, F_sigma_high], concept="sigma",
                                    universe_of_discourse=[0, 700])
lv_in3.plot()
FS.add_linguistic_variable("sigma", lv_in3)

F_P40_low = IntervalFuzzySet(function_start=fz.fun_P40_low, term="low")
F_P40_med = IntervalFuzzySet(function_start=fz.fun_P40_med, term="medium")
F_P40_high = IntervalFuzzySet(function_start=fz.fun_P40_high, term="high")
lv_in4 = IntervalLinguisticVariable([F_P40_low, F_P40_med, F_P40_high], concept="P40",
                                    universe_of_discourse=[0, 1])
lv_in4.plot()
FS.add_linguistic_variable("P40", lv_in4)

F_pose_isLy = IntervalFuzzySet(function_start=fz.fun_Pose_isLy, term="isLy")
F_pose_mayLy = IntervalFuzzySet(function_start=fz.fun_Pose_mayLy, term="mayLy")
F_pose_notLy = IntervalFuzzySet(function_start=fz.fun_Pose_notLy, term="notLy")
lv_out1 = IntervalLinguisticVariable([F_pose_isLy, F_pose_mayLy, F_pose_notLy], concept="pose",
                                     universe_of_discourse=[0, 1])
lv_out1.plot()
FS.add_linguistic_variable("pose", lv_out1)

# define rules
R1 = "IF (P40 IS low) AND (HW IS high) AND (sigma IS low) AND (HHmax IS high) THEN (pose IS notLy)"
R2 = "IF (P40 IS low) AND (HW IS high) AND (sigma IS low) AND (HHmax IS medium) THEN (pose IS notLy)"
R3 = "IF (P40 IS low) AND (HW IS high) AND (sigma IS low) AND (HHmax IS low) THEN (pose IS notLy)"
R4 = "IF (P40 IS low) AND (HW IS high) AND (sigma IS medium) AND (HHmax IS high) THEN (pose IS notLy)"
R5 = "IF (P40 IS low) AND (HW IS high) AND (sigma IS medium) AND (HHmax IS medium) THEN (pose IS notLy)"
R6 = "IF (P40 IS low) AND (HW IS high) AND (sigma IS medium) AND (HHmax IS low) THEN (pose IS mayLy)"
R7 = "IF (P40 IS low) AND (HW IS high) AND (sigma IS high) AND (HHmax IS high) THEN (pose IS notLy)"
R8 = "IF (P40 IS low) AND (HW IS high) AND (sigma IS high) AND (HHmax IS medium) THEN (pose IS mayLy)"
R9 = "IF (P40 IS low) AND (HW IS high) AND (sigma IS high) AND (HHmax IS low) THEN (pose IS mayLy)"
R10 = "IF (P40 IS low) AND (HW IS medium) AND (sigma IS low) AND (HHmax IS high) THEN (pose IS notLy)"
R11 = "IF (P40 IS low) AND (HW IS medium) AND (sigma IS low) AND (HHmax IS medium) THEN (pose IS notLy)"
R12 = "IF (P40 IS low) AND (HW IS medium) AND (sigma IS low) AND (HHmax IS low) THEN (pose IS mayLy)"
R13 = "IF (P40 IS low) AND (HW IS medium) AND (sigma IS medium) AND (HHmax IS high) THEN (pose IS notLy)"
R14 = "IF (P40 IS low) AND (HW IS medium) AND (sigma IS medium) AND (HHmax IS medium) THEN (pose IS mayLy)"
R15 = "IF (P40 IS low) AND (HW IS medium) AND (sigma IS medium) AND (HHmax IS low) THEN (pose IS mayLy)"
R16 = "IF (P40 IS low) AND (HW IS medium) AND (sigma IS high) AND (HHmax IS high) THEN (pose IS mayLy)"
R17 = "IF (P40 IS low) AND (HW IS medium) AND (sigma IS high) AND (HHmax IS medium) THEN (pose IS mayLy)"
R18 = "IF (P40 IS low) AND (HW IS medium) AND (sigma IS high) AND (HHmax IS low) THEN (pose IS mayLy)"
R19 = "IF (P40 IS low) AND (HW IS low) AND (sigma IS low) AND (HHmax IS high) THEN (pose IS notLy)"
R20 = "IF (P40 IS low) AND (HW IS low) AND (sigma IS low) AND (HHmax IS medium) THEN (pose IS mayLy)"
R21 = "IF (P40 IS low) AND (HW IS low) AND (sigma IS low) AND (HHmax IS low) THEN (pose IS mayLy)"
R22 = "IF (P40 IS low) AND (HW IS low) AND (sigma IS medium) AND (HHmax IS high) THEN (pose IS mayLy)"
R23 = "IF (P40 IS low) AND (HW IS low) AND (sigma IS medium) AND (HHmax IS medium) THEN (pose IS mayLy)"
R24 = "IF (P40 IS low) AND (HW IS low) AND (sigma IS medium) AND (HHmax IS low) THEN (pose IS mayLy)"
R25 = "IF (P40 IS low) AND (HW IS low) AND (sigma IS high) AND (HHmax IS high) THEN (pose IS mayLy)"
R26 = "IF (P40 IS low) AND (HW IS low) AND (sigma IS high) AND (HHmax IS medium) THEN (pose IS mayLy)"
R27 = "IF (P40 IS low) AND (HW IS low) AND (sigma IS high) AND (HHmax IS low) THEN (pose IS isLy)"
R28 = "IF (P40 IS medium) AND (HW IS high) AND (sigma IS low) AND (HHmax IS high) THEN (pose IS notLy)"
R29 = "IF (P40 IS medium) AND (HW IS high) AND (sigma IS low) AND (HHmax IS medium) THEN (pose IS notLy)"
R30 = "IF (P40 IS medium) AND (HW IS high) AND (sigma IS low) AND (HHmax IS low) THEN (pose IS mayLy)"
R31 = "IF (P40 IS medium) AND (HW IS high) AND (sigma IS medium) AND (HHmax IS high) THEN (pose IS notLy)"
R32 = "IF (P40 IS medium) AND (HW IS high) AND (sigma IS medium) AND (HHmax IS medium) THEN (pose IS mayLy)"
R33 = "IF (P40 IS medium) AND (HW IS high) AND (sigma IS medium) AND (HHmax IS low) THEN (pose IS mayLy)"
R34 = "IF (P40 IS medium) AND (HW IS high) AND (sigma IS high) AND (HHmax IS high) THEN (pose IS mayLy)"
R35 = "IF (P40 IS medium) AND (HW IS high) AND (sigma IS high) AND (HHmax IS medium) THEN (pose IS mayLy)"
R36 = "IF (P40 IS medium) AND (HW IS high) AND (sigma IS high) AND (HHmax IS low) THEN (pose IS mayLy)"
R37 = "IF (P40 IS medium) AND (HW IS medium) AND (sigma IS low) AND (HHmax IS high) THEN (pose IS notLy)"
R38 = "IF (P40 IS medium) AND (HW IS medium) AND (sigma IS low) AND (HHmax IS medium) THEN (pose IS mayLy)"
R39 = "IF (P40 IS medium) AND (HW IS medium) AND (sigma IS low) AND (HHmax IS low) THEN (pose IS mayLy)"
R40 = "IF (P40 IS medium) AND (HW IS medium) AND (sigma IS medium) AND (HHmax IS high) THEN (pose IS mayLy)"
R41 = "IF (P40 IS medium) AND (HW IS medium) AND (sigma IS medium) AND (HHmax IS medium) THEN (pose IS mayLy)"
R42 = "IF (P40 IS medium) AND (HW IS medium) AND (sigma IS medium) AND (HHmax IS low) THEN (pose IS mayLy)"
R43 = "IF (P40 IS medium) AND (HW IS medium) AND (sigma IS high) AND (HHmax IS high) THEN (pose IS mayLy)"
R44 = "IF (P40 IS medium) AND (HW IS medium) AND (sigma IS high) AND (HHmax IS medium) THEN (pose IS mayLy)"
R45 = "IF (P40 IS medium) AND (HW IS medium) AND (sigma IS high) AND (HHmax IS low) THEN (pose IS isLy)"
R46 = "IF (P40 IS medium) AND (HW IS low) AND (sigma IS low) AND (HHmax IS high) THEN (pose IS mayLy)"
R47 = "IF (P40 IS medium) AND (HW IS low) AND (sigma IS low) AND (HHmax IS medium) THEN (pose IS mayLy)"
R48 = "IF (P40 IS medium) AND (HW IS low) AND (sigma IS low) AND (HHmax IS low) THEN (pose IS mayLy)"
R49 = "IF (P40 IS medium) AND (HW IS low) AND (sigma IS medium) AND (HHmax IS high) THEN (pose IS mayLy)"
R50 = "IF (P40 IS medium) AND (HW IS low) AND (sigma IS medium) AND (HHmax IS medium) THEN (pose IS mayLy)"
R51 = "IF (P40 IS medium) AND (HW IS low) AND (sigma IS medium) AND (HHmax IS low) THEN (pose IS isLy)"
R52 = "IF (P40 IS medium) AND (HW IS low) AND (sigma IS high) AND (HHmax IS high) THEN (pose IS mayLy)"
R53 = "IF (P40 IS medium) AND (HW IS low) AND (sigma IS high) AND (HHmax IS medium) THEN (pose IS isLy)"
R54 = "IF (P40 IS medium) AND (HW IS low) AND (sigma IS high) AND (HHmax IS low) THEN (pose IS isLy)"
R55 = "IF (P40 IS high) AND (HW IS high) AND (sigma IS low) AND (HHmax IS high) THEN (pose IS notLy)"
R56 = "IF (P40 IS high) AND (HW IS high) AND (sigma IS low) AND (HHmax IS medium) THEN (pose IS mayLy)"
R57 = "IF (P40 IS high) AND (HW IS high) AND (sigma IS low) AND (HHmax IS low) THEN (pose IS mayLy)"
R58 = "IF (P40 IS high) AND (HW IS high) AND (sigma IS medium) AND (HHmax IS high) THEN (pose IS mayLy)"
R59 = "IF (P40 IS high) AND (HW IS high) AND (sigma IS medium) AND (HHmax IS medium) THEN (pose IS mayLy)"
R60 = "IF (P40 IS high) AND (HW IS high) AND (sigma IS medium) AND (HHmax IS low) THEN (pose IS mayLy)"
R61 = "IF (P40 IS high) AND (HW IS high) AND (sigma IS high) AND (HHmax IS high) THEN (pose IS mayLy)"
R62 = "IF (P40 IS high) AND (HW IS high) AND (sigma IS high) AND (HHmax IS medium) THEN (pose IS mayLy)"
R63 = "IF (P40 IS high) AND (HW IS high) AND (sigma IS high) AND (HHmax IS low) THEN (pose IS isLy)"
R64 = "IF (P40 IS high) AND (HW IS medium) AND (sigma IS low) AND (HHmax IS high) THEN (pose IS mayLy)"
R65 = "IF (P40 IS high) AND (HW IS medium) AND (sigma IS low) AND (HHmax IS medium) THEN (pose IS mayLy)"
R66 = "IF (P40 IS high) AND (HW IS medium) AND (sigma IS low) AND (HHmax IS low) THEN (pose IS mayLy)"
R67 = "IF (P40 IS high) AND (HW IS medium) AND (sigma IS medium) AND (HHmax IS high) THEN (pose IS mayLy)"
R68 = "IF (P40 IS high) AND (HW IS medium) AND (sigma IS medium) AND (HHmax IS medium) THEN (pose IS mayLy)"
R69 = "IF (P40 IS high) AND (HW IS medium) AND (sigma IS medium) AND (HHmax IS low) THEN (pose IS isLy)"
R70 = "IF (P40 IS high) AND (HW IS medium) AND (sigma IS high) AND (HHmax IS high) THEN (pose IS mayLy)"
R71 = "IF (P40 IS high) AND (HW IS medium) AND (sigma IS high) AND (HHmax IS medium) THEN (pose IS isLy)"
R72 = "IF (P40 IS high) AND (HW IS medium) AND (sigma IS high) AND (HHmax IS low) THEN (pose IS isLy)"
R73 = "IF (P40 IS high) AND (HW IS low) AND (sigma IS low) AND (HHmax IS high) THEN (pose IS mayLy)"
R74 = "IF (P40 IS high) AND (HW IS low) AND (sigma IS low) AND (HHmax IS medium) THEN (pose IS mayLy)"
R75 = "IF (P40 IS high) AND (HW IS low) AND (sigma IS low) AND (HHmax IS low) THEN (pose IS isLy)"
R76 = "IF (P40 IS high) AND (HW IS low) AND (sigma IS medium) AND (HHmax IS high) THEN (pose IS mayLy)"
R77 = "IF (P40 IS high) AND (HW IS low) AND (sigma IS medium) AND (HHmax IS medium) THEN (pose IS isLy)"
R78 = "IF (P40 IS high) AND (HW IS low) AND (sigma IS medium) AND (HHmax IS low) THEN (pose IS isLy)"
R79 = "IF (P40 IS high) AND (HW IS low) AND (sigma IS high) AND (HHmax IS high) THEN (pose IS isLy)"
R80 = "IF (P40 IS high) AND (HW IS low) AND (sigma IS high) AND (HHmax IS medium) THEN (pose IS isLy)"
R81 = "IF (P40 IS high) AND (HW IS low) AND (sigma IS high) AND (HHmax IS low) THEN (pose IS isLy)"

# using fuzzy system
FS.add_rules(
    [R1, R2, R3, R4, R5, R6, R7, R8, R9, R10, R11, R12, R13, R14, R15, R16, R17, R18, R19, R20, R21, R22, R23, R24, R25,
     R26, R27, R28, R29, R30, R31, R32, R33, R34, R35, R36, R37, R38, R39, R40, R41, R42, R43, R44, R45, R46, R47, R48,
     R49, R50, R51, R52, R53, R54, R55, R56, R57, R58, R59, R60, R61, R62, R63, R64, R65, R66, R67, R68, R69, R70, R71,
     R72, R73, R74, R75, R76, R77, R78, R79, R80, R81])

new_data_array = []
for row in data_array:
    if row[4] != 0:
        new_data_array.append(row)

data_array = new_data_array

filepath0 = "interval_results2.txt"

f_raw_data = open(filepath0, "a")
f_raw_data.write("[P40, HW, HHmax, sigma, Pose, result]\n")
# # pose = -1   =>  notly

i = 1
TP, TN, FN, FP = 0, 0, 0, 0

for row in data_array:
    # print(i)
    i += 1
    FS.set_variable("P40", (row[0], row[0]))
    FS.set_variable("HHmax", (row[1], row[1]))
    FS.set_variable("sigma", (row[2], row[2]))
    FS.set_variable("HW", (row[3], row[3]))
    result = FS.Mamdani_interval_inference(["pose"])
    # Correctly for interval, when start = end
    if result['pose'][0] >= 0.5:
        if row[4] == -1:
            TP += 1
        else:
            FP += 1
    elif result['pose'][0] < 0.5:
        if row[4] == -1:
            FN += 1
        else:
            TN += 1
    f_raw_data.write(str([row[0], row[3], row[1], row[2], row[4], result['pose']]) + "\n")

f_raw_data.close()
print("results: \nTP: ", TP, " \nTN: ", TN, "\nFP:", FP, "\nFN:", FN)
