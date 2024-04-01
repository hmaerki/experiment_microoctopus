# Plugins used

* https://github.com/bennymeg/JLC-Plugin-for-KiCad
  JLC PCB Plug-in for KiCad

  Fill Symbol Field `JLC Part`

## Export DXF from FreeCad

FreeCad -> Edit -> Preference
  Import-Export -> DXF
    [ ] Show this dialog when...
    [ ] Use legacy python importer
    [x] Use legacy python exporter
    [x] Allow FreeCad to automatically download
    ...
    [ ] Export 3D objects as polyface mashes
    [x] Export Drawing Views as blocks
    [x] Project export objects along current view direction

FreeCad et view: PCB top view
FreeCad -> File -> Export -> <filename>.dxf
