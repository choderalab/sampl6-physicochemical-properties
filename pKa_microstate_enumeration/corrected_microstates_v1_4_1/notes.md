# 2017/12/08

The microscopic pKa refers to the pKa of deprotonation of a single titratable group while all the other titratable and tautomerizable functional groups of the same molecule are held fixed.

Resonance structures or geometric isomers of compounds do not constitute seperate microstates. 
I will compare number of heavy atoms, total charge of the molecule and number of hydrogens bound to each heavy atom to detect unique or replicate microstate structures.


## Procedure

I will keep recording deprecated microstates in correction files:
corrections_for_v1_3_2 directory copied from ../corrected_microstates_v1_3_2

1. Run detecting_replicate_microstates.ipynb

2. Visually check potential replicates detected by the script and create SMXX_correction.csv files.

3. Create records for newly added corrections:
$mkdir corrections_for_v1_4_1_new
cp SM*_correction.csv corrections_for_v1_4_1_new

4. Create cumulative records of updates until now:
$mkdir corrections_for_v1_4_1_cumulative
$cp corrections_for_v1_3_2/*.csv corrections_for_v1_4_1_cumulative
$mkdir microstate_lists_after_correction

5. Run update_microstate_lists_to_remove_replicates.ipynb 


# 2017/12/12

## Detected replicate microstates

### SM10
('SM10_micro015', 'SM10_micro029') - correct! Resonance structures. Deprecate: SM10_micro029

### SM18
('SM18_micro001', 'SM18_micro041') - Geometric isomers. Deprecate: SM18_micro041   
('SM18_micro005', 'SM18_micro008') - Resonance structures. Deprecate: SM18_micro008
('SM18_micro009', 'SM18_micro035') - Geometric isomers. Deprecate: SM18_micro035  
('SM18_micro010', 'SM18_micro073') - Geometric isomers. Deprecate: SM18_micro073 
('SM18_micro011', 'SM18_micro039') - Geometric isomers. Deprecate: SM18_micro039 
('SM18_micro013', 'SM18_micro067') - Geometric isomers. Deprecate: SM18_micro067 
('SM18_micro015', 'SM18_micro061') - Geometric isomers. Deprecate: SM18_micro015 
('SM18_micro019', 'SM18_micro029') - Geometric isomers. Deprecate: SM18_micro019
('SM18_micro025', 'SM18_micro027') - Geometric isomers. Deprecate: SM18_micro027
('SM18_micro032', 'SM18_micro040') - Geometric isomers. Deprecate: SM18_micro040 
('SM18_micro037', 'SM18_micro044') - Geometric isomers. Deprecate: SM18_micro044 
('SM18_micro038', 'SM18_micro066') - Geometric isomers. Deprecate: SM18_micro066
('SM18_micro043', 'SM18_micro053') - Geometric isomers. Deprecate: SM18_micro043
('SM18_micro046', 'SM18_micro063') - Geometric isomers. Deprecate: SM18_micro046

### SM21
('SM21_micro016', 'SM21_micro025') - Geometric isomers. Deprecate: SM21_micro016 

### SM23
('SM23_micro001', 'SM23_micro008')
('SM23_micro001', 'SM23_micro020') ('SM23_micro008', 'SM23_micro020') - Resonance structure and geometric isomers. Deprecate: SM23_micro001, SM23_micro008
('SM23_micro004', 'SM23_micro011') - Geometric isomers. Deprecate: SM23_micro004.
('SM23_micro005', 'SM23_micro016') - Geometric isomers. Deprecate: SM23_micro016
('SM23_micro006', 'SM23_micro014')
('SM23_micro006', 'SM23_micro028')
('SM23_micro014', 'SM23_micro028') - Resonance structure and geometric isomers. Deprecate: SM23_micro006 and SM23_micro014
('SM23_micro015', 'SM23_micro027')
('SM23_micro015', 'SM23_micro029')
('SM23_micro015', 'SM23_micro036')
('SM23_micro027', 'SM23_micro029')
('SM23_micro027', 'SM23_micro036')
('SM23_micro029', 'SM23_micro036') - Resonance structure and geometric isomers. Deprecate: SM23_micro015, SM23_micro027, SM23_micro029

### SM24
('SM24_micro007', 'SM24_micro008') were geometric isomers. Deprecate: SM24_micro008.

