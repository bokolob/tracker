EESchema Schematic File Version 4
EELAYER 30 0
EELAYER END
$Descr A3 16535 11693
encoding utf-8
Sheet 1 1
Title ""
Date ""
Rev ""
Comp ""
Comment1 ""
Comment2 ""
Comment3 ""
Comment4 ""
$EndDescr
$Comp
L Transistor_FET:IRLML5203 Q1
U 1 1 5F3D5D19
P 6100 3300
F 0 "Q1" H 6304 3346 50  0000 L CNN
F 1 "IRLML5203" H 6304 3255 50  0000 L CNN
F 2 "Package_TO_SOT_SMD:SOT-23" H 6300 3225 50  0001 L CIN
F 3 "https://www.infineon.com/dgdl/irlml5203pbf.pdf?fileId=5546d462533600a40153566868da261d" H 6100 3300 50  0001 L CNN
	1    6100 3300
	-1   0    0    1   
$EndComp
Text Label 7750 2350 0    50   ~ 0
+5V
$Comp
L Device:C C7
U 1 1 5F3D5D20
P 8500 4400
F 0 "C7" V 8752 4400 50  0000 C CNN
F 1 "4.7uF" V 8661 4400 50  0000 C CNN
F 2 "Capacitor_SMD:C_1206_3216Metric_Pad1.42x1.75mm_HandSolder" H 8538 4250 50  0001 C CNN
F 3 "~" H 8500 4400 50  0001 C CNN
	1    8500 4400
	1    0    0    -1  
$EndComp
$Comp
L power:GNDREF #PWR0101
U 1 1 5F3D5D26
P 8500 4750
AR Path="/5F3D5D26" Ref="#PWR0101"  Part="1" 
AR Path="/5F3BC941/5F3D5D26" Ref="#PWR0115"  Part="1" 
F 0 "#PWR0101" H 8500 4500 50  0001 C CNN
F 1 "GNDREF" H 8505 4577 50  0000 C CNN
F 2 "" H 8500 4750 50  0001 C CNN
F 3 "" H 8500 4750 50  0001 C CNN
	1    8500 4750
	1    0    0    -1  
$EndComp
$Comp
L Device:C C6
U 1 1 5F3D5D2D
P 7600 3550
F 0 "C6" V 7852 3550 50  0000 C CNN
F 1 "C" V 7761 3550 50  0000 C CNN
F 2 "Capacitor_SMD:C_1206_3216Metric_Pad1.42x1.75mm_HandSolder" H 7638 3400 50  0001 C CNN
F 3 "~" H 7600 3550 50  0001 C CNN
	1    7600 3550
	0    -1   -1   0   
$EndComp
Connection ~ 7750 3550
$Comp
L power:GNDREF #PWR0116
U 1 1 5F3D5D34
P 7450 3750
F 0 "#PWR0116" H 7450 3500 50  0001 C CNN
F 1 "GNDREF" H 7455 3577 50  0000 C CNN
F 2 "" H 7450 3750 50  0001 C CNN
F 3 "" H 7450 3750 50  0001 C CNN
	1    7450 3750
	1    0    0    -1  
$EndComp
Wire Wire Line
	7450 3750 7450 3550
$Comp
L Device:R R6
U 1 1 5F3D5D3B
P 8450 3400
F 0 "R6" H 8380 3354 50  0000 R CNN
F 1 "250" H 8380 3445 50  0000 R CNN
F 2 "Resistor_SMD:R_0402_1005Metric" V 8380 3400 50  0001 C CNN
F 3 "~" H 8450 3400 50  0001 C CNN
	1    8450 3400
	1    0    0    -1  
$EndComp
Wire Wire Line
	8150 4450 8200 4450
$Comp
L Device:LED D6
U 1 1 5F3D5D42
P 8450 3800
F 0 "D6" H 8443 3545 50  0000 C CNN
F 1 "LED" H 8443 3636 50  0000 C CNN
F 2 "LED_SMD:LED_0603_1608Metric_Pad1.05x0.95mm_HandSolder" H 8450 3800 50  0001 C CNN
F 3 "~" H 8450 3800 50  0001 C CNN
	1    8450 3800
	0    -1   -1   0   
$EndComp
$Comp
L Device:R R3
U 1 1 5F3D5D48
P 7350 4800
F 0 "R3" H 7280 4754 50  0000 R CNN
F 1 "2000" H 7280 4845 50  0000 R CNN
F 2 "Resistor_SMD:R_0603_1608Metric" H 7280 4891 50  0001 R CNN
F 3 "~" H 7350 4800 50  0001 C CNN
	1    7350 4800
	-1   0    0    1   
$EndComp
Wire Wire Line
	7350 4450 7350 4650
Wire Wire Line
	7750 4650 7750 5000
Wire Wire Line
	7750 5000 7350 5000
Wire Wire Line
	7350 5000 7350 4950
$Comp
L power:GNDREF #PWR0117
U 1 1 5F3D5D52
P 7750 5150
F 0 "#PWR0117" H 7750 4900 50  0001 C CNN
F 1 "GNDREF" H 7755 4977 50  0000 C CNN
F 2 "" H 7750 5150 50  0001 C CNN
F 3 "" H 7750 5150 50  0001 C CNN
	1    7750 5150
	1    0    0    -1  
$EndComp
Wire Wire Line
	7750 5000 7750 5150
Connection ~ 7750 5000
Wire Wire Line
	6000 3500 6000 3750
Text Label 6000 2900 2    50   ~ 0
V_BAT
Wire Wire Line
	8150 4250 8500 4250
$Comp
L Battery_Management:MCP73831-2-OT U3
U 1 1 5F3D5D5D
P 7750 4350
F 0 "U3" H 7306 4304 50  0000 R CNN
F 1 "MCP73831-2-OT" H 8450 4050 50  0000 R CNN
F 2 "Package_TO_SOT_SMD:SOT-23-5" H 7800 4100 50  0001 L CIN
F 3 "http://ww1.microchip.com/downloads/en/DeviceDoc/20001984g.pdf" H 7600 4300 50  0001 C CNN
	1    7750 4350
	1    0    0    -1  
$EndComp
Wire Wire Line
	8500 4550 8500 4750
Wire Wire Line
	8500 4250 8800 4250
Wire Wire Line
	8800 4250 8800 4200
Connection ~ 8500 4250
$Comp
L Device:CP C9
U 1 1 5F3D5D67
P 12150 2400
F 0 "C9" H 12268 2446 50  0000 L CNN
F 1 "470uF" H 12268 2355 50  0000 L CNN
F 2 "Capacitor_THT:CP_Radial_D8.0mm_P3.50mm" H 12188 2250 50  0001 C CNN
F 3 "~" H 12150 2400 50  0001 C CNN
	1    12150 2400
	1    0    0    -1  
$EndComp
$Comp
L Device:CP C10
U 1 1 5F3D5D6D
P 12600 2400
F 0 "C10" H 12718 2446 50  0000 L CNN
F 1 "470uF" H 12718 2355 50  0000 L CNN
F 2 "Capacitor_THT:CP_Radial_D8.0mm_P3.50mm" H 12638 2250 50  0001 C CNN
F 3 "~" H 12600 2400 50  0001 C CNN
	1    12600 2400
	1    0    0    -1  
$EndComp
Wire Wire Line
	12150 2250 12150 2100
Wire Wire Line
	12600 2250 12600 2100
Wire Wire Line
	11550 2300 11550 2100
$Comp
L power:GNDREF #PWR0122
U 1 1 5F3D5D8B
P 6100 2950
F 0 "#PWR0122" H 6100 2700 50  0001 C CNN
F 1 "GNDREF" V 6150 3050 50  0000 C CNN
F 2 "" H 6100 2950 50  0001 C CNN
F 3 "" H 6100 2950 50  0001 C CNN
	1    6100 2950
	1    0    0    -1  
$EndComp
$Comp
L Device:C C8
U 1 1 5F3D5D91
P 11550 2450
F 0 "C8" H 11665 2496 50  0000 L CNN
F 1 "1uF" H 11665 2405 50  0000 L CNN
F 2 "Capacitor_Tantalum_SMD:CP_EIA-3216-18_Kemet-A" H 11588 2300 50  0001 C CNN
F 3 "~" H 11550 2450 50  0001 C CNN
	1    11550 2450
	1    0    0    -1  
$EndComp
Text GLabel 6000 3750 0    50   Input ~ 0
BAT_IN
$Comp
L Connector:USB_B_Mini J8
U 1 1 5F3D5D9C
P 11500 6200
F 0 "J8" H 11557 6667 50  0000 C CNN
F 1 "USB_B_Mini" H 11557 6576 50  0000 C CNN
F 2 "Connector_USB:USB_Micro-B_Molex-105017-0001" H 11650 6150 50  0001 C CNN
F 3 "~" H 11650 6150 50  0001 C CNN
	1    11500 6200
	1    0    0    -1  
$EndComp
$Comp
L power:GNDREF #PWR0123
U 1 1 5F3D5DA2
P 11500 6800
F 0 "#PWR0123" H 11500 6550 50  0001 C CNN
F 1 "GNDREF" H 11505 6627 50  0000 C CNN
F 2 "" H 11500 6800 50  0001 C CNN
F 3 "" H 11500 6800 50  0001 C CNN
	1    11500 6800
	1    0    0    -1  
$EndComp
Wire Wire Line
	11500 6600 11500 6700
Wire Wire Line
	11800 6000 12750 6000
Wire Wire Line
	6300 3300 6550 3300
Text Label 12450 6000 0    50   ~ 0
+5V
Wire Wire Line
	7750 3550 7750 4050
Text Label 8200 4150 0    50   ~ 0
CHARGER_STAT
Wire Wire Line
	11800 6400 11800 6700
Wire Wire Line
	11800 6700 11500 6700
Connection ~ 11500 6700
Wire Wire Line
	11500 6700 11500 6800
NoConn ~ 11800 6200
NoConn ~ 11800 6300
NoConn ~ 11400 6600
Connection ~ 7750 2450
$Comp
L power:GNDREF #PWR0102
U 1 1 5F3D5DB8
P 7450 3050
AR Path="/5F3D5DB8" Ref="#PWR0102"  Part="1" 
AR Path="/5F3BC941/5F3D5DB8" Ref="#PWR0124"  Part="1" 
F 0 "#PWR0102" H 7450 2800 50  0001 C CNN
F 1 "GNDREF" H 7455 2877 50  0000 C CNN
F 2 "" H 7450 3050 50  0001 C CNN
F 3 "" H 7450 3050 50  0001 C CNN
	1    7450 3050
	1    0    0    -1  
$EndComp
$Comp
L Device:R R5
U 1 1 5F3D5DBE
P 7450 2700
F 0 "R5" H 7400 2700 50  0000 L CNN
F 1 "100kOm" H 7300 2600 50  0000 L CNN
F 2 "Resistor_SMD:R_0603_1608Metric" H 7520 2609 50  0001 L CNN
F 3 "~" H 7450 2700 50  0001 C CNN
	1    7450 2700
	1    0    0    -1  
$EndComp
Wire Wire Line
	6100 2750 6100 2950
$Comp
L Connector:Screw_Terminal_01x02 J7
U 1 1 5F3D5DC8
P 6000 2550
F 0 "J7" V 5964 2362 50  0000 R CNN
F 1 "Screw_Terminal_01x02" V 6100 2800 50  0000 R CNN
F 2 "Connector_Wire:SolderWirePad_1x02_P5.08mm_Drill1.5mm" H 6000 2550 50  0001 C CNN
F 3 "~" H 6000 2550 50  0001 C CNN
	1    6000 2550
	0    -1   -1   0   
$EndComp
Wire Wire Line
	8200 3950 8200 4450
Text Label 7750 3350 0    50   ~ 0
CHARGER_VDD
Wire Wire Line
	7750 2150 7750 2450
$Comp
L Device:D_Schottky D5
U 1 1 5F3D5DD1
P 7750 3000
F 0 "D5" V 7796 2921 50  0000 R CNN
F 1 "D_Schottky" V 7705 2921 50  0000 R CNN
F 2 "Diode_SMD:D_SMA" H 7750 3000 50  0001 C CNN
F 3 "~" H 7750 3000 50  0001 C CNN
	1    7750 3000
	0    -1   -1   0   
$EndComp
Wire Wire Line
	7750 2450 7750 2700
Wire Wire Line
	7750 2700 8450 2700
Connection ~ 7750 2700
Wire Wire Line
	8200 3950 8450 3950
Wire Wire Line
	8450 3550 8450 3650
Wire Wire Line
	7450 2550 7450 2450
Connection ~ 7450 2450
Wire Wire Line
	7450 2450 7750 2450
Wire Wire Line
	7450 2850 7450 3050
Text Label 7350 4600 0    50   ~ 0
CHARGER_PROG
$Comp
L power:+5V #PWR0125
U 1 1 5F3D5DE3
P 7750 2150
F 0 "#PWR0125" H 7750 2000 50  0001 C CNN
F 1 "+5V" H 7765 2323 50  0000 C CNN
F 2 "" H 7750 2150 50  0001 C CNN
F 3 "" H 7750 2150 50  0001 C CNN
	1    7750 2150
	1    0    0    -1  
$EndComp
Wire Wire Line
	7750 2700 7750 2850
$Comp
L Tracker:A9G D4
U 1 1 5F3D6B88
P 4450 5500
F 0 "D4" H 4500 6106 50  0000 C CNN
F 1 "A9G" H 4500 6015 50  0000 C CNN
F 2 "Tracker:A9G2" V 3950 4450 50  0001 C CNN
F 3 "" V 3950 4450 50  0001 C CNN
	1    4450 5500
	1    0    0    -1  
$EndComp
Wire Wire Line
	3450 6750 3000 6750
Wire Wire Line
	3000 6750 3000 6850
Text GLabel 2950 7400 0    50   Input ~ 0
BAT_IN
$Comp
L Device:R R7
U 1 1 5F429F48
P 7050 2650
F 0 "R7" H 6980 2604 50  0000 R CNN
F 1 "250" H 6980 2695 50  0000 R CNN
F 2 "Resistor_SMD:R_0402_1005Metric" V 6980 2650 50  0001 C CNN
F 3 "~" H 7050 2650 50  0001 C CNN
	1    7050 2650
	1    0    0    -1  
$EndComp
$Comp
L Device:LED D7
U 1 1 5F429F4E
P 7050 3050
F 0 "D7" H 7043 2795 50  0000 C CNN
F 1 "LED" H 7043 2886 50  0000 C CNN
F 2 "LED_SMD:LED_0603_1608Metric_Pad1.05x0.95mm_HandSolder" H 7050 3050 50  0001 C CNN
F 3 "~" H 7050 3050 50  0001 C CNN
	1    7050 3050
	0    -1   -1   0   
$EndComp
Wire Wire Line
	7050 2800 7050 2900
$Comp
L power:GNDREF #PWR0104
U 1 1 5F42B001
P 7050 3500
AR Path="/5F42B001" Ref="#PWR0104"  Part="1" 
AR Path="/5F3BC941/5F42B001" Ref="#PWR0127"  Part="1" 
F 0 "#PWR0104" H 7050 3250 50  0001 C CNN
F 1 "GNDREF" H 7055 3327 50  0000 C CNN
F 2 "" H 7050 3500 50  0001 C CNN
F 3 "" H 7050 3500 50  0001 C CNN
	1    7050 3500
	1    0    0    -1  
$EndComp
Wire Wire Line
	7050 3200 7050 3500
$Comp
L Sensor_Motion:LIS3DH U2
U 1 1 5F3C2349
P 2650 3100
F 0 "U2" H 2650 2411 50  0000 C CNN
F 1 "LIS3DSH" H 2850 2700 50  0000 C CNN
F 2 "Package_LGA:LGA-16_3x3mm_P0.5mm_LayoutBorder3x5y" H 2750 2050 50  0001 C CNN
F 3 "https://www.st.com/resource/en/datasheet/cd00274221.pdf" H 2450 3000 50  0001 C CNN
	1    2650 3100
	1    0    0    -1  
$EndComp
$Comp
L Connector:SIM_Card J1
U 1 1 5F3DE822
P 9900 6200
F 0 "J1" H 10530 6300 50  0000 L CNN
F 1 "SIM_Card" H 10530 6209 50  0000 L CNN
F 2 "Connector_Card:microSIM_JAE_SF53S006VCBR2000" H 9900 6550 50  0001 C CNN
F 3 " ~" H 9850 6200 50  0001 C CNN
	1    9900 6200
	1    0    0    -1  
$EndComp
Text Label 6500 3300 0    50   ~ 0
+5V
Wire Wire Line
	6000 2750 6000 3100
Wire Wire Line
	8450 2700 8450 3250
Wire Wire Line
	7750 3150 7750 3550
Text Label 8750 4250 2    50   ~ 0
V_BAT
Wire Wire Line
	7050 2450 7050 2500
Wire Wire Line
	7050 2450 7450 2450
Text Label 10050 3650 0    50   ~ 0
CHARGER_VDD
Wire Wire Line
	10050 3650 10250 3650
Text GLabel 12350 3650 2    50   Input ~ 0
BAT_IN
$Comp
L power:GNDREF #PWR0108
U 1 1 5F53B583
P 10900 4700
AR Path="/5F53B583" Ref="#PWR0108"  Part="1" 
AR Path="/5F3BC941/5F53B583" Ref="#PWR?"  Part="1" 
F 0 "#PWR0108" H 10900 4450 50  0001 C CNN
F 1 "GNDREF" H 10905 4527 50  0000 C CNN
F 2 "" H 10900 4700 50  0001 C CNN
F 3 "" H 10900 4700 50  0001 C CNN
	1    10900 4700
	1    0    0    -1  
$EndComp
Wire Wire Line
	9400 5900 9150 5900
Text Label 9250 5900 0    50   ~ 0
VSIM
Text Label 5850 5850 0    50   ~ 0
VSIM
Text Label 9150 6000 0    50   ~ 0
SIM_RST
Wire Wire Line
	9150 6000 9400 6000
Text Label 5100 4950 0    50   ~ 0
SIM_RST
Wire Wire Line
	9400 6100 9150 6100
Text Label 9150 6100 0    50   ~ 0
SIM_CLK
Text Label 5850 5750 0    50   ~ 0
SIM_CLK
Wire Wire Line
	5300 5750 5850 5750
NoConn ~ 9400 6300
Wire Wire Line
	3200 7250 3200 7400
Wire Wire Line
	5000 7500 5000 7700
$Comp
L power:GNDREF #PWR0109
U 1 1 5F507040
P 5000 7700
F 0 "#PWR0109" H 5000 7450 50  0001 C CNN
F 1 "GNDREF" H 5005 7527 50  0000 C CNN
F 2 "" H 5000 7700 50  0001 C CNN
F 3 "" H 5000 7700 50  0001 C CNN
	1    5000 7700
	1    0    0    -1  
$EndComp
$Comp
L power:GNDREF #PWR0110
U 1 1 5F508ADE
P 3200 7400
F 0 "#PWR0110" H 3200 7150 50  0001 C CNN
F 1 "GNDREF" H 3205 7227 50  0000 C CNN
F 2 "" H 3200 7400 50  0001 C CNN
F 3 "" H 3200 7400 50  0001 C CNN
	1    3200 7400
	1    0    0    -1  
$EndComp
$Comp
L power:GNDREF #PWR0111
U 1 1 5F5096A9
P 2750 6650
F 0 "#PWR0111" H 2750 6400 50  0001 C CNN
F 1 "GNDREF" H 2755 6477 50  0000 C CNN
F 2 "" H 2750 6650 50  0001 C CNN
F 3 "" H 2750 6650 50  0001 C CNN
	1    2750 6650
	1    0    0    -1  
$EndComp
$Comp
L power:GNDREF #PWR0112
U 1 1 5F509F7D
P 4750 5600
F 0 "#PWR0112" H 4750 5350 50  0001 C CNN
F 1 "GNDREF" H 4650 5400 50  0000 C CNN
F 2 "" H 4750 5600 50  0001 C CNN
F 3 "" H 4750 5600 50  0001 C CNN
	1    4750 5600
	1    0    0    -1  
$EndComp
Wire Wire Line
	9400 6400 8950 6400
Text Label 9050 6400 0    50   ~ 0
SIM_IO
Text Label 5850 5950 0    50   ~ 0
SIM_IO
Wire Wire Line
	5300 5950 5850 5950
$Comp
L power:GNDREF #PWR0113
U 1 1 5F510A0E
P 8800 6200
F 0 "#PWR0113" H 8800 5950 50  0001 C CNN
F 1 "GNDREF" H 8805 6027 50  0000 C CNN
F 2 "" H 8800 6200 50  0001 C CNN
F 3 "" H 8800 6200 50  0001 C CNN
	1    8800 6200
	1    0    0    -1  
$EndComp
Wire Wire Line
	8800 6200 9400 6200
Wire Wire Line
	2750 6650 3150 6650
Wire Wire Line
	5300 5850 5850 5850
$Comp
L mailboxNotifier-eagle-import:U.FL GSM1
U 1 1 5F4E0DE8
P 4800 4300
F 0 "GSM1" H 4850 4350 50  0001 C CNN
F 1 "U.FL" H 4800 4300 50  0001 C CNN
F 2 "mailboxNotifier:U.FL" H 4800 4300 50  0001 C CNN
F 3 "" H 4800 4300 50  0001 C CNN
	1    4800 4300
	0    1    1    0   
$EndComp
$Comp
L mailboxNotifier-eagle-import:U.FL U1
U 1 1 5F4E2777
P 11850 7550
F 0 "U1" H 11900 7600 50  0001 C CNN
F 1 "U.FL" H 11850 7550 50  0001 C CNN
F 2 "mailboxNotifier:U.FL" H 11850 7550 50  0001 C CNN
F 3 "" H 11850 7550 50  0001 C CNN
	1    11850 7550
	-1   0    0    -1  
$EndComp
Wire Wire Line
	4600 4200 4500 4200
Wire Wire Line
	4500 4200 4250 4200
Connection ~ 4500 4200
$Comp
L power:GNDREF #PWR0114
U 1 1 5F4EBA24
P 4250 4300
F 0 "#PWR0114" H 4250 4050 50  0001 C CNN
F 1 "GNDREF" H 4255 4127 50  0000 C CNN
F 2 "" H 4250 4300 50  0001 C CNN
F 3 "" H 4250 4300 50  0001 C CNN
	1    4250 4300
	1    0    0    -1  
$EndComp
Wire Wire Line
	4250 4200 4250 4300
Wire Wire Line
	2950 6900 2950 6850
Wire Wire Line
	2950 6850 3000 6850
Connection ~ 3000 6850
Wire Wire Line
	3450 7200 3450 7250
Wire Wire Line
	3450 7250 3200 7250
Connection ~ 3450 7250
Wire Wire Line
	3450 7250 3450 7300
$Comp
L power:GNDREF #PWR0115
U 1 1 5F505EB6
P 5600 7000
F 0 "#PWR0115" H 5600 6750 50  0001 C CNN
F 1 "GNDREF" H 5605 6827 50  0000 C CNN
F 2 "" H 5600 7000 50  0001 C CNN
F 3 "" H 5600 7000 50  0001 C CNN
	1    5600 7000
	1    0    0    -1  
$EndComp
Wire Wire Line
	5300 6950 5600 6950
Wire Wire Line
	5600 6950 5600 7000
$Comp
L Connector:Conn_01x05_Male J2
U 1 1 5F50A53E
P 3750 8100
F 0 "J2" V 3812 8344 50  0000 L CNN
F 1 "Conn_01x05_Male" V 3903 8344 50  0000 L CNN
F 2 "Connector_PinHeader_2.54mm:PinHeader_1x05_P2.54mm_Vertical" H 3750 8100 50  0001 C CNN
F 3 "~" H 3750 8100 50  0001 C CNN
	1    3750 8100
	0    1    1    0   
$EndComp
Wire Wire Line
	4800 4500 4800 5150
Wire Wire Line
	5100 4950 5100 5150
Wire Wire Line
	4700 5150 4700 5600
Wire Wire Line
	4700 5600 4750 5600
Wire Wire Line
	4900 5600 4900 5150
Wire Wire Line
	4900 5150 4900 4850
Connection ~ 4900 5150
Wire Wire Line
	3700 5150 3700 4900
Wire Wire Line
	3850 5150 3850 4900
Wire Wire Line
	3550 8300 3550 8500
$Comp
L power:GNDREF #PWR0118
U 1 1 5F5743E5
P 3450 8500
F 0 "#PWR0118" H 3450 8250 50  0001 C CNN
F 1 "GNDREF" H 3455 8327 50  0000 C CNN
F 2 "" H 3450 8500 50  0001 C CNN
F 3 "" H 3450 8500 50  0001 C CNN
	1    3450 8500
	1    0    0    -1  
$EndComp
Text Label 5850 6050 0    50   ~ 0
HST_RXD
Text Label 3650 8600 1    50   ~ 0
HST_RXD
Wire Wire Line
	3650 8300 3650 8600
Text Label 5850 6150 0    50   ~ 0
HST_TXD
Wire Wire Line
	5300 6150 5850 6150
Wire Wire Line
	5300 6050 5850 6050
Text Label 3750 8600 1    50   ~ 0
HST_TXD
Wire Wire Line
	3750 8300 3750 8600
Text Label 3700 4900 1    50   ~ 0
UART1_TXD
Text Label 3850 8700 1    50   ~ 0
UART1_TXD
Text Label 3850 4900 1    50   ~ 0
UART1_RXD
Text Label 3950 8700 1    50   ~ 0
UART1_RXD
Wire Wire Line
	3850 8300 3850 8700
Wire Wire Line
	3950 8300 3950 8700
Wire Wire Line
	3450 8500 3550 8500
$Comp
L Device:C C11
U 1 1 5F5001FA
P 10850 2450
F 0 "C11" H 10965 2496 50  0000 L CNN
F 1 "100uF" H 10965 2405 50  0000 L CNN
F 2 "Capacitor_Tantalum_SMD:CP_EIA-3216-18_Kemet-A" H 10888 2300 50  0001 C CNN
F 3 "~" H 10850 2450 50  0001 C CNN
	1    10850 2450
	1    0    0    -1  
$EndComp
$Comp
L power:GNDREF #PWR0103
U 1 1 5F500667
P 10850 2750
F 0 "#PWR0103" H 10850 2500 50  0001 C CNN
F 1 "GNDREF" H 10855 2577 50  0000 C CNN
F 2 "" H 10850 2750 50  0001 C CNN
F 3 "" H 10850 2750 50  0001 C CNN
	1    10850 2750
	1    0    0    -1  
$EndComp
Wire Wire Line
	12600 2100 12150 2100
Wire Wire Line
	11550 2100 12150 2100
Connection ~ 12150 2100
Wire Wire Line
	11550 2100 10850 2100
Wire Wire Line
	10850 2100 10850 2300
Connection ~ 11550 2100
$Comp
L Device:C C12
U 1 1 5F520BC8
P 10350 2450
F 0 "C12" H 10465 2496 50  0000 L CNN
F 1 "33pF" H 10465 2405 50  0000 L CNN
F 2 "Capacitor_Tantalum_SMD:CP_EIA-3216-18_Kemet-A" H 10388 2300 50  0001 C CNN
F 3 "~" H 10350 2450 50  0001 C CNN
	1    10350 2450
	1    0    0    -1  
$EndComp
Wire Wire Line
	10350 2100 10350 2300
$Comp
L Device:C C13
U 1 1 5F525B81
P 9800 2450
F 0 "C13" H 9915 2496 50  0000 L CNN
F 1 "10pF" H 9915 2405 50  0000 L CNN
F 2 "Capacitor_Tantalum_SMD:CP_EIA-3216-18_Kemet-A" H 9838 2300 50  0001 C CNN
F 3 "~" H 9800 2450 50  0001 C CNN
	1    9800 2450
	1    0    0    -1  
$EndComp
Wire Wire Line
	9800 2600 9800 2700
Wire Wire Line
	9800 2100 9800 2300
Wire Wire Line
	9800 2100 10350 2100
Connection ~ 10850 2100
Connection ~ 10350 2100
Wire Wire Line
	10350 2100 10850 2100
Wire Wire Line
	9800 2700 10350 2700
Wire Wire Line
	12600 2700 12600 2550
Wire Wire Line
	12150 2550 12150 2700
Connection ~ 12150 2700
Wire Wire Line
	12150 2700 12600 2700
Wire Wire Line
	11550 2600 11550 2700
Connection ~ 11550 2700
Wire Wire Line
	11550 2700 12150 2700
Wire Wire Line
	10350 2600 10350 2700
Connection ~ 10350 2700
Wire Wire Line
	10350 2700 10850 2700
Wire Wire Line
	10850 2600 10850 2700
Connection ~ 10850 2700
Wire Wire Line
	10850 2700 11550 2700
Wire Wire Line
	10850 2700 10850 2750
$Comp
L Regulator_Linear:LM350_TO220 U4
U 1 1 5F57590C
P 10900 3650
F 0 "U4" H 10900 3892 50  0000 C CNN
F 1 "LM350_TO220" H 10900 3801 50  0000 C CNN
F 2 "Package_TO_SOT_THT:TO-220-3_Horizontal_TabDown" H 10900 3900 50  0001 C CIN
F 3 "http://www.fairchildsemi.com/ds/LM/LM350.pdf" H 10900 3650 50  0001 C CNN
	1    10900 3650
	1    0    0    -1  
$EndComp
$Comp
L Device:R R2
U 1 1 5F57AA87
P 11350 3900
F 0 "R2" H 11280 3854 50  0000 R CNN
F 1 "47000" H 11280 3945 50  0000 R CNN
F 2 "Resistor_SMD:R_0603_1608Metric" H 11280 3991 50  0001 R CNN
F 3 "~" H 11350 3900 50  0001 C CNN
	1    11350 3900
	-1   0    0    1   
$EndComp
$Comp
L Device:R R1
U 1 1 5F57B204
P 10900 4400
F 0 "R1" H 10830 4354 50  0000 R CNN
F 1 "10000" H 10830 4445 50  0000 R CNN
F 2 "Resistor_SMD:R_0603_1608Metric" H 10830 4491 50  0001 R CNN
F 3 "~" H 10900 4400 50  0001 C CNN
	1    10900 4400
	-1   0    0    1   
$EndComp
Wire Wire Line
	10900 3950 10900 4050
Wire Wire Line
	10900 4700 10900 4550
Wire Wire Line
	10900 4050 11350 4050
Connection ~ 10900 4050
Wire Wire Line
	10900 4050 10900 4250
Wire Wire Line
	11200 3650 11350 3650
Wire Wire Line
	11350 3650 11350 3750
Wire Wire Line
	11350 3650 11800 3650
Connection ~ 11350 3650
$Comp
L Device:D_Schottky D1
U 1 1 5F5BE753
P 11950 3650
F 0 "D1" V 11996 3571 50  0000 R CNN
F 1 "D_Schottky" V 11905 3571 50  0000 R CNN
F 2 "Diode_SMD:D_SMA" H 11950 3650 50  0001 C CNN
F 3 "~" H 11950 3650 50  0001 C CNN
	1    11950 3650
	-1   0    0    1   
$EndComp
Wire Wire Line
	12100 3650 12350 3650
$Comp
L Device:C C14
U 1 1 5F5C2E5D
P 10250 3800
F 0 "C14" H 10365 3846 50  0000 L CNN
F 1 "1uF" H 10365 3755 50  0000 L CNN
F 2 "Capacitor_Tantalum_SMD:CP_EIA-3216-18_Kemet-A" H 10288 3650 50  0001 C CNN
F 3 "~" H 10250 3800 50  0001 C CNN
	1    10250 3800
	1    0    0    -1  
$EndComp
Connection ~ 10250 3650
Wire Wire Line
	10250 3650 10600 3650
$Comp
L power:GNDREF #PWR0105
U 1 1 5F5C392C
P 10250 4100
AR Path="/5F5C392C" Ref="#PWR0105"  Part="1" 
AR Path="/5F3BC941/5F5C392C" Ref="#PWR?"  Part="1" 
F 0 "#PWR0105" H 10250 3850 50  0001 C CNN
F 1 "GNDREF" H 10255 3927 50  0000 C CNN
F 2 "" H 10250 4100 50  0001 C CNN
F 3 "" H 10250 4100 50  0001 C CNN
	1    10250 4100
	1    0    0    -1  
$EndComp
Wire Wire Line
	10250 4100 10250 3950
Wire Wire Line
	3250 2350 3200 2350
Wire Wire Line
	2550 2350 2550 2600
$Comp
L power:GNDREF #PWR0106
U 1 1 5F54A3D7
P 2650 3850
F 0 "#PWR0106" H 2650 3600 50  0001 C CNN
F 1 "GNDREF" H 2655 3677 50  0000 C CNN
F 2 "" H 2650 3850 50  0001 C CNN
F 3 "" H 2650 3850 50  0001 C CNN
	1    2650 3850
	1    0    0    -1  
$EndComp
Wire Wire Line
	2650 3700 2650 3850
Wire Wire Line
	3150 3000 3350 3000
Wire Wire Line
	3450 3000 3450 3050
$Comp
L power:GNDREF #PWR0107
U 1 1 5F55B58A
P 3450 3050
F 0 "#PWR0107" H 3450 2800 50  0001 C CNN
F 1 "GNDREF" H 3455 2877 50  0000 C CNN
F 2 "" H 3450 3050 50  0001 C CNN
F 3 "" H 3450 3050 50  0001 C CNN
	1    3450 3050
	1    0    0    -1  
$EndComp
Wire Wire Line
	3150 3100 3250 3100
Wire Wire Line
	3250 3100 3250 2350
Wire Wire Line
	2750 2600 2750 2350
Connection ~ 2750 2350
Wire Wire Line
	2750 2350 2550 2350
Wire Wire Line
	3150 3200 3350 3200
Wire Wire Line
	3350 3200 3350 3000
Connection ~ 3350 3000
Wire Wire Line
	3350 3000 3450 3000
$Comp
L Device:C C1
U 1 1 5F56C46E
P 2900 2200
F 0 "C1" H 3015 2246 50  0000 L CNN
F 1 "10uF" H 3015 2155 50  0000 L CNN
F 2 "Capacitor_SMD:C_0603_1608Metric" H 2938 2050 50  0001 C CNN
F 3 "https://www.chipdip.ru/product/grm21br71a106ke51l" H 2900 2200 50  0001 C CNN
	1    2900 2200
	1    0    0    -1  
$EndComp
Connection ~ 2900 2350
Wire Wire Line
	2900 2350 2750 2350
$Comp
L Device:C C2
U 1 1 5F56E883
P 3200 2200
F 0 "C2" H 3315 2246 50  0000 L CNN
F 1 "100nF" H 3315 2155 50  0000 L CNN
F 2 "Capacitor_SMD:C_0603_1608Metric" H 3238 2050 50  0001 C CNN
F 3 "https://www.chipdip.ru/product/grm188r71c104ka01d" H 3200 2200 50  0001 C CNN
	1    3200 2200
	1    0    0    -1  
$EndComp
Connection ~ 3200 2350
Wire Wire Line
	3200 2350 2900 2350
Wire Wire Line
	2900 2050 3200 2050
Connection ~ 3200 2050
Wire Wire Line
	3200 2050 3600 2050
$Comp
L power:GNDREF #PWR0119
U 1 1 5F574A7E
P 3600 2100
F 0 "#PWR0119" H 3600 1850 50  0001 C CNN
F 1 "GNDREF" H 3605 1927 50  0000 C CNN
F 2 "" H 3600 2100 50  0001 C CNN
F 3 "" H 3600 2100 50  0001 C CNN
	1    3600 2100
	1    0    0    -1  
$EndComp
Wire Wire Line
	3600 2050 3600 2100
NoConn ~ 2150 3000
Wire Wire Line
	3450 6550 3150 6550
Wire Wire Line
	3150 6550 3150 6650
Connection ~ 3150 6650
Wire Wire Line
	3150 6650 3450 6650
Wire Wire Line
	7600 7300 8350 7300
Wire Wire Line
	2950 7300 2950 7400
Text Label 2350 7100 0    50   ~ 0
PWR_CTRL
Text Label 7700 7400 0    50   ~ 0
PWR_CTRL
Wire Wire Line
	7600 7400 7700 7400
Wire Wire Line
	5300 6850 5800 6850
Wire Wire Line
	5800 6850 5800 8450
Wire Wire Line
	5800 8450 7850 8450
Wire Wire Line
	7850 8450 7850 7500
Wire Wire Line
	7850 7500 7600 7500
Wire Wire Line
	5300 6750 5900 6750
Wire Wire Line
	5900 6750 5900 8350
Wire Wire Line
	5900 8350 7800 8350
Wire Wire Line
	7800 8350 7800 7600
Wire Wire Line
	7800 7600 7600 7600
$Comp
L power:GNDREF #PWR0120
U 1 1 5F5C5802
P 7000 8200
F 0 "#PWR0120" H 7000 7950 50  0001 C CNN
F 1 "GNDREF" H 7005 8027 50  0000 C CNN
F 2 "" H 7000 8200 50  0001 C CNN
F 3 "" H 7000 8200 50  0001 C CNN
	1    7000 8200
	1    0    0    -1  
$EndComp
Wire Wire Line
	2350 7100 2650 7100
Wire Wire Line
	3000 6850 3450 6850
Text Label 1700 2900 0    50   ~ 0
ACCEL_INT1
Text Label 1700 3100 0    50   ~ 0
ACCEL_SDO
Text Label 1700 3200 0    50   ~ 0
ACCEL_SDA
Text Label 1700 3300 0    50   ~ 0
ACCEL_SCL
Text Label 1700 3400 0    50   ~ 0
ACCEL_CS
Wire Wire Line
	1700 2900 2150 2900
Wire Wire Line
	1700 3100 2150 3100
Wire Wire Line
	1700 3200 2150 3200
Wire Wire Line
	1700 3300 2150 3300
Wire Wire Line
	1700 3400 2150 3400
Text Label 8300 7300 0    50   ~ 0
ACCEL_INT1
Connection ~ 4750 5600
Wire Wire Line
	4750 5600 4900 5600
Text Label 2950 5950 0    50   ~ 0
ACCEL_SDO
Text Label 2950 5750 0    50   ~ 0
ACCEL_SCL
Text Label 2950 5850 0    50   ~ 0
ACCEL_SDA
Text Label 2950 6050 0    50   ~ 0
ACCEL_CS
Wire Wire Line
	2950 5750 3450 5750
Wire Wire Line
	3450 5850 2950 5850
Wire Wire Line
	2950 5950 3450 5950
Wire Wire Line
	3450 6050 2950 6050
$Comp
L Device:R R4
U 1 1 5F827328
P 1600 8000
F 0 "R4" H 1530 7954 50  0000 R CNN
F 1 "200K" H 1530 8045 50  0000 R CNN
F 2 "Resistor_SMD:R_0603_1608Metric" H 1530 8091 50  0001 R CNN
F 3 "~" H 1600 8000 50  0001 C CNN
	1    1600 8000
	0    -1   -1   0   
$EndComp
Wire Wire Line
	1200 8000 1450 8000
Wire Wire Line
	1750 8000 1800 8000
Wire Wire Line
	2200 8000 2400 8000
$Comp
L power:GNDREF #PWR0121
U 1 1 5F83F6D0
P 2400 8150
F 0 "#PWR0121" H 2400 7900 50  0001 C CNN
F 1 "GNDREF" H 2405 7977 50  0000 C CNN
F 2 "" H 2400 8150 50  0001 C CNN
F 3 "" H 2400 8150 50  0001 C CNN
	1    2400 8150
	1    0    0    -1  
$EndComp
Wire Wire Line
	2400 8000 2400 8150
Text Label 1200 8000 2    50   ~ 0
V_BAT
Wire Wire Line
	3800 7500 3800 7750
Wire Wire Line
	3800 7750 1800 7750
Wire Wire Line
	1800 7750 1800 8000
Connection ~ 1800 8000
Wire Wire Line
	1800 8000 1900 8000
$Comp
L Device:R R11
U 1 1 5F8A46E3
P 2700 6150
F 0 "R11" V 2630 6104 50  0000 R CNN
F 1 "125" V 2600 6400 50  0000 R CNN
F 2 "Resistor_SMD:R_0805_2012Metric_Pad1.15x1.40mm_HandSolder" H 2630 6241 50  0001 R CNN
F 3 "~" H 2700 6150 50  0001 C CNN
	1    2700 6150
	0    -1   -1   0   
$EndComp
$Comp
L Device:R R10
U 1 1 5F8A4C51
P 2650 6350
F 0 "R10" V 2580 6304 50  0000 R CNN
F 1 "125" V 2550 6600 50  0000 R CNN
F 2 "Resistor_SMD:R_0805_2012Metric_Pad1.15x1.40mm_HandSolder" H 2580 6441 50  0001 R CNN
F 3 "~" H 2650 6350 50  0001 C CNN
	1    2650 6350
	0    -1   -1   0   
$EndComp
$Comp
L Device:R R9
U 1 1 5F8A5B95
P 2600 6550
F 0 "R9" V 2530 6504 50  0000 R CNN
F 1 "125" V 2450 6800 50  0000 R CNN
F 2 "Resistor_SMD:R_0805_2012Metric_Pad1.15x1.40mm_HandSolder" H 2530 6641 50  0001 R CNN
F 3 "~" H 2600 6550 50  0001 C CNN
	1    2600 6550
	0    -1   -1   0   
$EndComp
Wire Wire Line
	2350 6150 2550 6150
Wire Wire Line
	2350 6350 2500 6350
Wire Wire Line
	2350 6550 2450 6550
Wire Wire Line
	2750 6550 2950 6550
Wire Wire Line
	2950 6550 2950 6450
Wire Wire Line
	2950 6450 3450 6450
Wire Wire Line
	2800 6350 3450 6350
Wire Wire Line
	2850 6150 3050 6150
Wire Wire Line
	3050 6150 3050 6250
Wire Wire Line
	3050 6250 3450 6250
$Comp
L Regulator_Linear:MCP1700-2502E_SOT23 U7
U 1 1 5F58416E
P 7300 5950
F 0 "U7" H 7300 6192 50  0000 C CNN
F 1 "MCP1700-2502E_SOT23" H 7300 6101 50  0000 C CNN
F 2 "Package_TO_SOT_SMD:SOT-23" H 7300 6175 50  0001 C CNN
F 3 "http://ww1.microchip.com/downloads/en/DeviceDoc/20001826D.pdf" H 7300 5950 50  0001 C CNN
	1    7300 5950
	1    0    0    -1  
$EndComp
$Comp
L power:GNDREF #PWR0124
U 1 1 5F584E99
P 7300 6300
F 0 "#PWR0124" H 7300 6050 50  0001 C CNN
F 1 "GNDREF" H 7305 6127 50  0000 C CNN
F 2 "" H 7300 6300 50  0001 C CNN
F 3 "" H 7300 6300 50  0001 C CNN
	1    7300 6300
	1    0    0    -1  
$EndComp
Text GLabel 6850 5950 0    50   Input ~ 0
BAT_IN
Wire Wire Line
	6850 5950 6900 5950
Wire Wire Line
	7600 5950 7750 5950
Text Label 7000 7000 0    50   ~ 0
2.2V
Text Label 3250 2600 0    50   ~ 0
2.2V
$Comp
L Device:C C3
U 1 1 5F5A5D34
P 6900 6100
F 0 "C3" H 7015 6146 50  0000 L CNN
F 1 "10uF" H 7015 6055 50  0000 L CNN
F 2 "Capacitor_Tantalum_SMD:CP_EIA-3216-18_Kemet-A" H 6938 5950 50  0001 C CNN
F 3 "~" H 6900 6100 50  0001 C CNN
	1    6900 6100
	1    0    0    -1  
$EndComp
Connection ~ 6900 5950
Wire Wire Line
	6900 5950 7000 5950
Connection ~ 7750 5950
Wire Wire Line
	7750 5950 7850 5950
$Comp
L power:GNDREF #PWR0126
U 1 1 5F5A6F7D
P 6900 6300
F 0 "#PWR0126" H 6900 6050 50  0001 C CNN
F 1 "GNDREF" H 6905 6127 50  0000 C CNN
F 2 "" H 6900 6300 50  0001 C CNN
F 3 "" H 6900 6300 50  0001 C CNN
	1    6900 6300
	1    0    0    -1  
$EndComp
$Comp
L power:GNDREF #PWR0127
U 1 1 5F5A731B
P 7750 6300
F 0 "#PWR0127" H 7750 6050 50  0001 C CNN
F 1 "GNDREF" H 7755 6127 50  0000 C CNN
F 2 "" H 7750 6300 50  0001 C CNN
F 3 "" H 7750 6300 50  0001 C CNN
	1    7750 6300
	1    0    0    -1  
$EndComp
Wire Wire Line
	7750 6250 7750 6300
Wire Wire Line
	6900 6250 6900 6300
Wire Wire Line
	7300 6250 7300 6300
$Comp
L Device:R R8
U 1 1 5F827D55
P 2050 8000
F 0 "R8" H 1980 7954 50  0000 R CNN
F 1 "100K" H 1980 8045 50  0000 R CNN
F 2 "Resistor_SMD:R_0603_1608Metric" H 1980 8091 50  0001 R CNN
F 3 "~" H 2050 8000 50  0001 C CNN
	1    2050 8000
	0    -1   -1   0   
$EndComp
$Comp
L mailboxNotifier-eagle-import:INDUCTOR L1
U 1 1 5F5FBCCB
P 11150 7700
F 0 "L1" H 11150 7885 42  0000 C CNN
F 1 "LQG15HN27NJ" H 11150 7806 42  0000 C CNN
F 2 "Inductor_SMD:L_0402_1005Metric" H 11150 7700 50  0001 C CNN
F 3 "" H 11150 7700 50  0001 C CNN
	1    11150 7700
	1    0    0    -1  
$EndComp
Wire Wire Line
	11950 7750 11950 7850
Wire Wire Line
	11950 7850 12000 7850
Connection ~ 11950 7850
$Comp
L power:GNDREF #PWR0128
U 1 1 5F5C4C53
P 12000 7900
F 0 "#PWR0128" H 12000 7650 50  0001 C CNN
F 1 "GNDREF" H 12005 7727 50  0000 C CNN
F 2 "" H 12000 7900 50  0001 C CNN
F 3 "" H 12000 7900 50  0001 C CNN
	1    12000 7900
	1    0    0    -1  
$EndComp
Wire Wire Line
	12000 7850 12000 7900
Wire Wire Line
	5300 7050 5300 7300
Text Label 5300 7300 0    50   ~ 0
GPS_RF
$Comp
L MCU_Microchip_ATtiny:ATtiny85-20SU U6
U 1 1 5F57EEE2
P 7000 7600
F 0 "U6" H 6850 7500 50  0000 R CNN
F 1 "ATtiny85-20SU" H 7650 7000 50  0000 R CNN
F 2 "Package_SO:SOIJ-8_5.3x5.3mm_P1.27mm" H 7000 7600 50  0001 C CIN
F 3 "http://ww1.microchip.com/downloads/en/DeviceDoc/atmel-2586-avr-8-bit-microcontroller-attiny25-attiny45-attiny85_datasheet.pdf" H 7000 7600 50  0001 C CNN
	1    7000 7600
	1    0    0    -1  
$EndComp
Wire Wire Line
	11650 7550 11350 7550
Wire Wire Line
	11350 7550 11350 7700
Wire Wire Line
	11350 7550 10750 7550
Connection ~ 11350 7550
Text Label 10750 7550 0    50   ~ 0
GPS_RF
$Comp
L Device:R R13
U 1 1 5F612A4A
P 10650 7700
F 0 "R13" H 10580 7654 50  0000 R CNN
F 1 "100K" H 10580 7745 50  0000 R CNN
F 2 "Resistor_SMD:R_0603_1608Metric" H 10580 7791 50  0001 R CNN
F 3 "~" H 10650 7700 50  0001 C CNN
	1    10650 7700
	0    -1   -1   0   
$EndComp
$Comp
L Device:C C15
U 1 1 5F6131F1
P 10850 7850
F 0 "C15" V 11102 7850 50  0000 C CNN
F 1 "4.7uF" V 11011 7850 50  0000 C CNN
F 2 "Capacitor_SMD:C_1206_3216Metric_Pad1.42x1.75mm_HandSolder" H 10888 7700 50  0001 C CNN
F 3 "~" H 10850 7850 50  0001 C CNN
	1    10850 7850
	1    0    0    -1  
$EndComp
$Comp
L Device:C C5
U 1 1 5F613A69
P 10150 7850
F 0 "C5" V 10402 7850 50  0000 C CNN
F 1 "4.7uF" V 10311 7850 50  0000 C CNN
F 2 "Capacitor_SMD:C_1206_3216Metric_Pad1.42x1.75mm_HandSolder" H 10188 7700 50  0001 C CNN
F 3 "~" H 10150 7850 50  0001 C CNN
	1    10150 7850
	1    0    0    -1  
$EndComp
Wire Wire Line
	10800 7700 10850 7700
Wire Wire Line
	10950 7700 10850 7700
Connection ~ 10850 7700
Connection ~ 10150 7700
Wire Wire Line
	10150 7700 10500 7700
$Comp
L power:GNDREF #PWR0129
U 1 1 5F6589CC
P 10850 8150
F 0 "#PWR0129" H 10850 7900 50  0001 C CNN
F 1 "GNDREF" H 10855 7977 50  0000 C CNN
F 2 "" H 10850 8150 50  0001 C CNN
F 3 "" H 10850 8150 50  0001 C CNN
	1    10850 8150
	1    0    0    -1  
$EndComp
$Comp
L power:GNDREF #PWR0130
U 1 1 5F659058
P 10150 8150
F 0 "#PWR0130" H 10150 7900 50  0001 C CNN
F 1 "GNDREF" H 10155 7977 50  0000 C CNN
F 2 "" H 10150 8150 50  0001 C CNN
F 3 "" H 10150 8150 50  0001 C CNN
	1    10150 8150
	1    0    0    -1  
$EndComp
Wire Wire Line
	10150 8000 10150 8150
Wire Wire Line
	10850 8000 10850 8150
Wire Wire Line
	9700 7700 10150 7700
Wire Wire Line
	9300 7700 9050 7700
$Comp
L Device:R R12
U 1 1 5F6A076F
P 9250 7200
F 0 "R12" H 9180 7154 50  0000 R CNN
F 1 "100K" H 9180 7245 50  0000 R CNN
F 2 "Resistor_SMD:R_0603_1608Metric" H 9180 7291 50  0001 R CNN
F 3 "~" H 9250 7200 50  0001 C CNN
	1    9250 7200
	0    -1   -1   0   
$EndComp
$Comp
L power:GNDREF #PWR0131
U 1 1 5F6A1210
P 8850 7350
F 0 "#PWR0131" H 8850 7100 50  0001 C CNN
F 1 "GNDREF" H 8855 7177 50  0000 C CNN
F 2 "" H 8850 7350 50  0001 C CNN
F 3 "" H 8850 7350 50  0001 C CNN
	1    8850 7350
	1    0    0    -1  
$EndComp
Wire Wire Line
	8850 7200 8850 7350
Wire Wire Line
	8850 7200 9100 7200
Wire Wire Line
	9400 7200 9500 7200
Wire Wire Line
	9500 7200 9500 7050
Wire Wire Line
	9500 7200 9500 7400
Connection ~ 9500 7200
Text Label 3100 6850 0    50   ~ 0
VBAT
Text Label 9050 7700 0    50   ~ 0
VBAT
Wire Wire Line
	5300 6650 5550 6650
Text Label 5550 6650 0    50   ~ 0
GPS_CTRL
Text Label 9500 7400 0    50   ~ 0
GPS_CTRL
$Comp
L Transistor_FET:IRLML0030 Q2
U 1 1 5F6E0FC1
P 2850 7100
F 0 "Q2" H 3055 7146 50  0000 L CNN
F 1 "IRLML0030" H 2200 6950 50  0000 L CNN
F 2 "Package_TO_SOT_SMD:SOT-23" H 3050 7025 50  0001 L CIN
F 3 "https://www.infineon.com/dgdl/irlml0030pbf.pdf?fileId=5546d462533600a401535664773825df" H 2850 7100 50  0001 L CNN
	1    2850 7100
	1    0    0    -1  
$EndComp
$Comp
L Transistor_FET:IRLML0030 Q3
U 1 1 5F6FE985
P 9500 7600
F 0 "Q3" H 9705 7646 50  0000 L CNN
F 1 "IRLML0030" V 9850 7300 50  0000 L CNN
F 2 "Package_TO_SOT_SMD:SOT-23" H 9700 7525 50  0001 L CIN
F 3 "https://www.infineon.com/dgdl/irlml0030pbf.pdf?fileId=5546d462533600a401535664773825df" H 9500 7600 50  0001 L CNN
	1    9500 7600
	0    1    1    0   
$EndComp
$Comp
L Device:LED_RGB LED1
U 1 1 5F594CBF
P 2150 6350
F 0 "LED1" H 2150 5883 50  0000 C CNN
F 1 "TO-5050BC-MRPBFGF" H 2150 5974 50  0000 C CNN
F 2 "LED_SMD:LED_RGB_5050-6" H 2150 6300 50  0001 C CNN
F 3 "https://www.chipdip.ru/product/to-5050bc-mrpbfgf" H 2150 6300 50  0001 C CNN
	1    2150 6350
	-1   0    0    1   
$EndComp
Wire Wire Line
	1950 6550 1950 6350
Connection ~ 1950 6350
Wire Wire Line
	1950 6150 1950 6350
Text Label 12600 2100 0    50   ~ 0
VBAT
$Comp
L Regulator_Switching:APW7142 D2
U 1 1 5F6172A8
P 8800 1550
F 0 "D2" H 8625 2025 50  0000 C CNN
F 1 "APW7142" H 8625 1934 50  0000 C CNN
F 2 "Package_SO:SOP-8_3.76x4.96mm_P1.27mm" H 8800 1550 50  0001 C CNN
F 3 "" H 8800 1550 50  0001 C CNN
	1    8800 1550
	1    0    0    -1  
$EndComp
$Comp
L Device:C C4
U 1 1 5F5A6A6D
P 7750 6100
F 0 "C4" H 7865 6146 50  0000 L CNN
F 1 "10uF" H 7865 6055 50  0000 L CNN
F 2 "Capacitor_Tantalum_SMD:CP_EIA-3216-18_Kemet-A" H 7788 5950 50  0001 C CNN
F 3 "~" H 7750 6100 50  0001 C CNN
	1    7750 6100
	1    0    0    -1  
$EndComp
Wire Wire Line
	1500 6350 1950 6350
Text Label 1500 6350 0    50   ~ 0
2.2V
Text Label 7850 5950 0    50   ~ 0
2.2V
$EndSCHEMATC