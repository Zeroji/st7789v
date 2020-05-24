"""List of Table 1 commands for ST7789V chip."""

#pylint: disable=C0326
commands = [
    # (ID, NAME,        W, R, "DESC")
    (0x01, 'SWRESET',   0, 0, "Software Reset"),
    (0x04, 'RDDID',     0, 4, "Read Display ID"),
    (0x05, 'RDDST',     0, 5, "Read Display Status"),
    (0x0A, 'RDDPM',     0, 2, "Read Display Power Mode"),
    (0x0B, 'RDDMADCTL', 0, 2, "Read Display MADCTL"),
    (0x0C, 'RDDCOLMOD', 0, 2, "Read Display Pixel Format"),
    (0x0D, 'RDDIM',     0, 2, "Read Display Image Mode"),
    (0x0E, 'RDDSM',     0, 2, "Read Display Signal Mode"),
    (0x0F, 'RDDSDR',    0, 2, "Read Display Self-Diagnostic Result"),
    (0x10, 'SLPIN',     0, 0, "Sleep in"),  # Default
    (0x11, 'SLPOUT',    0, 0, "Sleep out"),
    (0x12, 'PTLON',     0, 0, "Partial Display Mode On"),  # See 30h
    (0x13, 'NORON',     0, 0, "Normal Display Mode On"),  # Default
    (0x20, 'INVOFF',    0, 0, "Display Inversion Off"),  # Default
    (0x21, 'INVON',     0, 0, "Display Inversion On"),
    (0x26, 'GAMSET',    1, 0, "Gamma Set"),
    (0x28, 'DISPOFF',   0, 0, "Display Off"),  # Default
    (0x29, 'DISPON',    0, 0, "Display On"),
    (0x2A, 'CASET',     4, 0, "Column Address Set"),  # uint16 * 2
    (0x2B, 'RASET',     4, 0, "Row Address Set"),  # uint16 * 2
    (0x2C, 'RAMWR',    -1, 0, "Memory Write"),  # Not cleared on SW/HW reset, resets col/row
    (0x2E, 'RAWRD',     0,-1, "Memory Read"),  # Resets col/row registers, fixed 18-bit
    (0x30, 'PTLAR',     4, 0, "Partial Area"),  # uint16 * 2
    (0x33, 'VSCRDEF',   6, 0, "Vertical Scrolling Definition"),  # uint16 * 3
    (0x34, 'TEOFF',     0, 0, "Tearing Effect Line OFF"),  # Default
    (0x35, 'TEON',      1, 0, "Tearing Effect Line On"),
    (0x36, 'MADCTL',    1, 0, "Memory Data Access Control"),
    (0x37, 'VSCSAD',    2, 0, "Vertical Scroll Start Address of RAM"),
    (0x38, 'IDMOFF',    0, 0, "Idle Mode OFF"),  # Default
    (0x39, 'IDMON',     0, 0, "Idle Mode ON"),  # Reduced to 8 colors (RGB-111)
    (0x3A, 'COLMOD',    1, 0, "Interface Pixel Format"),  # Default 66h (RGB-666)
    (0x3C, 'WRMEMC',   -1, 0, "Write Memory Continue"),  # After 2Ch
    (0x3E, 'RDMEMC',    0,-1, "Read Memory Continue"),  # After 2Eh
    (0x44, 'STE',       2, 0, "Set Tear Scanline"),
    (0x45, 'GSCAN',     0, 3, "Get Scanline"),
    (0x51, 'WRDISBV',   1, 0, "Write Display Brightness"),
    (0x52, 'RDDISBV',   0, 2, "Read Display Brightness Value"),
    (0x53, 'WRCTRLD',   1, 0, "Write CTRL Display"),
    (0x54, 'RDCTRLD',   0, 2, "Read CTRL Value Display"),
    (0x55, 'WRCACE',    1, 0, "Write Content Adaptive Brightness Control and Color Enhancement"),
    (0x56, 'RDCABC',    0, 2, "Read Content Adaptive Brightness Control"),
    (0x5E, 'WRCACBCMB', 1, 0, "Write CABC Minimum Brightness"),
    (0x5F, 'RDCABCMB',  0, 2, "Read CABC Minimum Brightness"),
    (0x68, 'RDABCSDR',  0, 2, "Read Automatic Brightness Control Self-Diagnotstic Result"),
    (0xDA, 'RDID1',     0, 2, "Read ID1"),
    (0xDB, 'RDID2',     0, 2, "Read ID2"),
    (0xDC, 'RDID3',     0, 2, "Read ID3"),
]

by_name = {
    name: {'id': id, 'wrx': wrx, 'rdx': rdx, 'desc': desc}
    for id, name, wrx, rdx, desc in commands
}

by_id = {
    id: {'name': name, 'wrx': wrx, 'rdx': rdx, 'desc': desc}
    for id, name, wrx, rdx, desc in commands
}
