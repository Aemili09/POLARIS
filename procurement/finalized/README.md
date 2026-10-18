# POLARIS finalized component specification

[Download the Google-Sheets-importable workbook](https://github.com/Aemili09/POLARIS/raw/refs/heads/main/procurement/finalized/POLARIS_Finalized_Component_List_Google_Sheets_Import.xlsx)

[Download the core list as CSV](https://github.com/Aemili09/POLARIS/raw/refs/heads/main/procurement/finalized/POLARIS_Core_BOM.csv) — one tab only; prefer the workbook for all explanations.

This is an XLSX workbook, **not an already-created Google Sheet**. There is no Google Sheets connection available in the current assistant session. To create your own Google Sheet:

1. Download the workbook above.
2. Open https://sheets.new while signed into your Google account.
3. Select **File → Import → Upload** and choose the workbook.
4. Choose **Create new spreadsheet** and import it. All eight tabs are included.
5. Keep the imported file in your Drive and use **Share** to invite your teammates if desired.

Alternatively, upload the workbook to Google Drive, open it with Google Sheets, and choose **File → Save as Google Sheets** if it remains in Office-editing mode.

## What changed

The former shopping list mixed installed requirements, spare quantities, alternative materials and accessories that might already be included. It also did not explicitly account for all mechanical supports.

| Circuit part | Installed quantity | Previous suggested purchase quantity |
| --- | ---: | ---: |
| FQP30N06L MOSFET | 1 | 2, including a spare |
| NC home microswitch | 1 | 2, including a spare |
| 10 kΩ resistor | 4 | 10 |
| 4.7 kΩ resistor | 1 | 5 |
| 100 Ω resistor | 1 | 5 |
| 100 µF / 35 V capacitor | 1 | 2 |
| 100 nF capacitor | 2 | 5 |
| Fuse | 1 | 3 |

- Two **polarizing optical pieces** are required; one cuttable retail sheet may be sufficient if both footprints and mounting margins fit. The holder/aperture design decides this.
- A separate diffuser and USB cable are purchased only if not included or already available.
- The rotating polarizer holder is part of the annular ring assembly; do not buy it twice.
- Start with polycarbonate; acrylic is optional comparison material.
- Signal hookup wire and jumper pigtails are consolidated into one harness requirement.
- A specimen holder, backlight support, home-switch bracket/actuator, driver headers/sockets and a belt-tension provision are now explicit. Integrate them into fabrication quotes where practical.
- Load cell/HX711 remain an optional force-acquisition module. A **rated loading fixture and appropriate force measurement are necessary for controlled applied-load tests**; the basic holder is not that fixture.

## The eight tabs

1. **START HERE:** scope, limitations and Google Sheets import steps.
2. **Core BOM:** 38 core specification lines, installed quantities, purchase/bundle rules and compatibility gates.
3. **Optional and spares:** spare parts, optional modules and conditional purchases.
4. **Changes vs previous list:** every earlier item reconciled.
5. **Connections:** terminal-to-terminal circuit mapping with BOM IDs.
6. **Purchase gates:** what must be checked before ordering, assembly and measurement claims.
7. **Supplier searches:** unverified search links for five suppliers per core item; not verified product listings or endorsements.
8. **Actual quotes:** blank price/order fields and an INCOMPLETE total until all required quantities, prices, additional tax and delivery amounts are entered.

## What remains unresolved

This is an audited **procurement specification**, not a bench-tested guarantee or a fully dimensioned mechanical design. Confirm camera manual controls and optical working distance, analyzer ring/bearing geometry, clear aperture, belt length, base dimensions and bundled accessories before ordering those items. The Logitech C270 is a candidate, not a guaranteed compatible measurement camera.

Scope is an initial motorized qualitative polarization-imaging setup. No hardware has been assembled or validated; motion/acquisition firmware, alignment, repeatability testing and calibration remain necessary. A trained AI model and calibrated stress outputs are not delivered by purchasing components alone. Reuse an existing laptop and laboratory tools where available.

No updated market-price total is claimed. The earlier INR 15,000 figure was an unverified planning allowance and is **not** a quotation for this corrected list.
