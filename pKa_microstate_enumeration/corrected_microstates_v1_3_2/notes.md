## 2017/11/22

# Removing Replicate Microstates From Microstates Lists

Stereoisomers and resonance structures don't constitute distinct microstates. 
In microstate lists v1.3.1 replic stereoisomers and resonance structures were removed by manual inspection. 
In v1.3.2 such replicate microstates will be filtered programmatically with OpenEye.

Correction files for v1.3.2 will include aggregate corrections made in v1.3.1 and v1.3.2

## Detected replicate microstates and other corrections

### SM11
- SM11_micro018 and SM11_micro020 were the same structure. I deprecated SM11_micro020.
- Added missing microstate: SM11_micro031

### SM18
- SM18_micro008, SM18_micro023, SM18_micro024, and SM18_micro036 are resonance structures. SM18_micro023, SM18_micro024, and SM18_micro036 will be deprecated.
- SM18_micro002, SM18_micro018, and SM18_micro022 are resonance structures. SM18_micro018 and SM18_micro022 will be deprecated.
- SM18_micro004, SM18_micro006, and SM18_micro014 are resonance structures. SM18_micro006 and SM18_micro014 will be deprecated.

### SM23
- These are all resonance structures of the same microstate: "SM23_micro001", "SM23_micro003", "SM23_micro009", "SM23_micro023", "SM23_micro031", "SM23_micro032", "SM23_micro037". The following will be deprecated: "SM23_micro003", "SM23_micro009", "SM23_micro023", "SM23_micro031", "SM23_micro032", "SM23_micro037".

### SM24
- SM24_micro001, SM24_micro012 and SM24_micro018 are resonance structures. SM24_micro012 and SM24_micro018 will be deprecated.
- SM24_micro007, SM24_micro019 and SM24_micro021 are resonance structures. SM24_micro019 and SM24_micro021 will be deprecated.
- SM24_micro011 and SM24_micro015 are resonance structures. SM24_micro015 will be deprecated.


## Procedure

Follow these notebooks:
detecting_resonance_structures.ipynb  
checking_detected_resonance_structures.ipynb 
update_microstate_lists_based_on_oe_resonance_detection.ipynb

path to updated microstate files (v1_3_2): microstate_lists_after_correction/"
