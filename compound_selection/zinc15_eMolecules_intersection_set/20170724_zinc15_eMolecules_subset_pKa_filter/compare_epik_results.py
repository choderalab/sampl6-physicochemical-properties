"""
compare_epik_results: program to compare reference results with calculated results

First run epik with:
$SCHRODINGER/epik -ph 7.0 -scan -imae <input>.mae -omae <epik_output>.mae
Note: <epik_output>.log documents the results from the Epik calculation.

Run this script with:
python $SCHRODINGER/epik-vX.X/bin/<machine_type>/compare_epik_results.py \\
 <reference.csv> <epik_output>.log <summary_file> [-inorder] [-skip_first]

<reference.csv> is a comma separated file with one line for each ligand of the 
form:
   title,pKa1,pKa2,...

<summary_file is the 

By default the result sets are compared by matching up the titles for each 
ligand.  Note the titles listed for each ligang in <reference.csv> and 
<epik_output>.log must exactly match unless -inorder (see below) is 
specified.

-inorder match the results in the <reference.csv> and <epik_output>.log 
   based upon their order in these files. 

-skip_first
   Skip the first line in <reference.csv>.  Useful if the first line 
   contains column titles.

"""
import sys
import math

# handle arguments
if len( sys.argv ) <= 1: 
    print __doc__
    sys.exit() 

cnt_file = 0
inorder = 0
skip_ref_1 = 0
in_ref_name = ""
in_epik_name = ""
out_results_name = ""

for arg in sys.argv[1:]:
    if arg == "-inorder":
        inorder = 1
    elif arg == "-skip_first":
        skip_ref_1 = 1
    elif not arg.startswith( "-" ):
        if cnt_file == 0:
            in_ref_name = arg
            cnt_file += 1
        elif cnt_file == 1:
            in_epik_name = arg
            cnt_file += 1
        elif cnt_file == 2:
            out_results_name = arg
            cnt_file += 1
        else:
            print "\nError: 3 file names already given." 
            print "Error: Not sure what to do with argument: %s\n" % ( arg )
            print __doc__
            sys.exit() 

    elif "-help" in sys.argv:
        print __doc__
        sys.exit() 
    elif "-HELP" in sys.argv:
        print __doc__
        sys.exit() 
    elif "-h" in sys.argv:
        print __doc__
        sys.exit() 
    elif "-H" in sys.argv:
        print __doc__
        sys.exit() 
    else:
        print "\nError: Unknown option: %s\n" % ( arg )
        print __doc__
        sys.exit() 

if not in_ref_name:
    print "\nError: The reference (.csv) file name has not been provided.\n"
    print __doc__
    sys.exit() 

if not in_epik_name:
    print "\nError: The epik output (.log) file name has not been provided.\n"
    print __doc__
    sys.exit() 

if not out_results_name:
    print "\nError: The summary file name has not been provided.\n"
    print __doc__
    sys.exit() 

#print "in_ref_name %s" % in_ref_name
#print "in_epik_name %s" % in_epik_name
#print "out_results_name %s" % out_results_name


# open, read input files, close input files.
in_ref = open( in_ref_name, "r" )
in_epik = open( in_epik_name, "r" )
out_results = open( out_results_name, "w" )

ref = in_ref.read()
epik = in_epik.read()
in_ref.close()
in_epik.close()

ref_lines = ref.split( "\n" )
# ref_lines = ref_lines[ 1: ]
if skip_ref_1:
    ref_lines = ref_lines[ 1: ]


cnt = 1
undef = -10000
match_shift = 4.1

# extract and organize reference information
ref_res = {}

ref_names = []
for refline in ref_lines:
    aset = refline.split( "," )
    orig_name = aset[ 0 ]
    orig_name = orig_name.strip( '"' )
    orig_name = orig_name.strip()
    if not inorder:
        name = orig_name
        start = 1
    else:
        name = cnt
        cnt += 1
        start = 0
    nlines = len( aset )
    values = []
    for v in aset[ 1: ]:
        v = v.strip( '"' )
        if v:
            values.append( float(v) )
    if orig_name:
        ref_res[ name ]  = values
        ref_names.append( name )

#print ref_res

# extract and organize epik's pKa predictions 
epik = epik.split( "Processing Input Structure #" )
epik = epik[ 1: ]
epik_res = {}
cnt = 1
for epikline in epik:
    aset = epikline.split( "\n" )
    name = aset[ 1 ]
    name = name.strip()
    if not name.startswith( "Title:" ):
        break;
    name = name.replace( "Title:","" )
    if inorder:
        name = cnt
        cnt += 1
    else :
        name = name.strip()
    nlines = len( aset )
    values = []
    for il in range( 5, nlines ):
        aline = aset[ il ]
        chunks = aline.split() 
        nchunks = len( chunks )
        if nchunks > 0:
            if chunks[ 0 ].startswith( "-----" ):
               break;
            values.append( float(chunks[0]) )
    epik_res[ name ]  = values


print >> out_results, "Individual ligand results\n"
print >> out_results, "-" * 80

# report cases where a ligand only appears in one of the two files

ref_keys = ref_res.keys()
for each_key in ref_keys:
    if not epik_res.has_key( each_key ):
       print >> out_results, "Reference key: %s is not in Epik results file." % each_key
       print >> out_results, "  Reference pKa values:",
       for value in ref_res[ each_key ]:
          print >> out_results, " %5.2f" % value,
       print >> out_results, ""
       print >> out_results, "-" * 80

epik_keys = epik_res.keys()
for each_key in epik_keys:
    if not ref_res.has_key( each_key ):
       print >> out_results, "Epik key: %s is not in reference results file." % each_key
       print >> out_results, "  Reference pKa values:",
       for value in epik_res[ each_key ]:
          print >> out_results, " %5.2f" % value,
       print >> out_results, ""
       print >> out_results, "-" * 80


#print ref_keys

# process each ligand
# save prediction differences in all_dists list
all_dists = []
for each_key in ref_names:
    if not epik_res.has_key( each_key ):
        continue
    print >> out_results, "Processing Structure: %s" % each_key
    exp_v = ref_res[ each_key]
    exp_v.sort()
    #print "key %s values %s" % ( each_key, exp_v )
    predict = epik_res[ each_key ]
    if len( exp_v ) <= 0:
        print >> out_results, "ID: %s" % each_key
        print >> out_results, "No Experimental pKas"
        print >> out_results, "pKa values predicted:"
        for a_pKa in predict:
            print >> out_results, "    %5.2f" % a_pKa
        print >> out_results, "-" * 80
        continue

    predict = epik_res[ each_key ]
    predict.sort()

    maps = []
    more_maps = True
    start_value = -len( exp_v ) + 1
    end_value = len( predict ) + len( exp_v ) - 2
    pos_map = [ start_value ] 
    pos_map = pos_map * len( exp_v )

    el_up = range( 0, len(pos_map) )
    if len( el_up ) > 1:
        el_down = el_up[ : ]
        el_down.reverse()
    else:
        el_down = el_up

    while more_maps:
        # Is the map acceptable?
        map_OK = True
        for value in pos_map:
            if( value > end_value ):
                map_OK = False
                break
        if map_OK:
            for el in el_up[ : -1 ]:
                if pos_map[ el ] >= pos_map[ el + 1 ]:
                    map_OK = False
                    break
            if map_OK:
                map_OK = False
                for el in el_up:
                    if 0 <= pos_map[ el ] <= ( len(predict) -1 ):
                        map_OK = True
                        break
                if map_OK:
                    maps.append( pos_map[:] )
        # make a new map
        for el in el_down:
            pos_map[ el ] += 1
            if pos_map[ el ] <= end_value:
                break
            elif el == 0:
                more_maps = 0
                break
            else:
                pos_map[ el ] = 0

#    for a_map in maps:
#       print a_map

# make up a list of hits that includes the map, difference vector, difference 
# magnitude and number of matching pKas
    hits = []
    for a_map in maps:
        dist = [ undef ] * len( exp_v )
        sum_dist = 0.0
        num_match = 0
        for el in el_up:
            if 0 <= a_map[ el ] <= ( len(predict) -1 ):
               dist[ el ] =  exp_v[ el ] - predict[ a_map[el] ]
               sum_dist += abs( dist[el] )
               num_match += 1
        hits.append(  [a_map, dist, sum_dist, num_match] )

#    for a_hit in hits:
#        print "Hit %s" % a_hit


# for each num_match select the hit with the lowest error.
    indexed_hits = {}
    for a_hit in hits:
        num_match = a_hit[ -1 ]
        if indexed_hits.has_key( num_match ):
            if indexed_hits[ num_match ][ "sum_dist" ] > a_hit[ 2 ]:
              indexed_hits[ num_match ] = \
              { "map":a_hit[0], "dist":a_hit[1], "sum_dist":a_hit[2] }
        else:
            indexed_hits[ num_match ] = \
            { "map":a_hit[0], "dist":a_hit[1], "sum_dist":a_hit[2] }

#    for ih in indexed_hits:
#        print "num_match %s match %s" % ( ih, indexed_hits[ih] )

    min_dist = float( undef )
    min_num = undef

# select best match with a bias towards more matching pKas
# however the difference between the sum of the differences for the 
# two hits exceeds the difference in the number of matches * match_shift
# (match_shift typically = 4.1) retain the hit with the smaller number of
# matches as the better one.

    for ih in indexed_hits:
        if min_num == undef:
            min_num = ih
            min_dist = indexed_hits[ ih ][ "sum_dist" ]
        else:
            OK_diff = abs( min_num - ih ) * match_shift
            if abs( min_dist - indexed_hits[ih]["sum_dist"] ) < OK_diff:
                min_num = ih
                min_dist = indexed_hits[ ih ][ "sum_dist" ]

    if len( exp_v ) <= 0:
        print >> out_results, "No Experimental Data"
        if len( predict ) <= 0:
            print >> out_results, "No Predictions"
        else:
            print >> out_results, "Predictions"
            for p_pKa in predict:
                print >> out_results, p_pKa
    else:
        print >> out_results, "Matched pKas"
        print >> out_results, "    Exp     Predict    Difference"
        if min_num != undef:
            the_map = indexed_hits[ min_num ][ "map" ]
            dists = indexed_hits[ min_num ][ "dist" ]
        predict_match = [ False ] * len( predict )
        for el in el_up:
            if min_num != undef and ( 0 <= the_map[el] <= (len(predict)-1) ):
                triple = ( exp_v[el], predict[the_map[el]], dists[el] )
                print >> out_results, "    %5.2f    %5.2f    %5.2f" % triple
                predict_match[ the_map[el] ] = True
                all_dists.append( dists[el] )
            else:
                print >> out_results, "    %5.2f      N/A      N/A" % ( exp_v[el] )

        un_matched_predictions = False
        for pm in predict_match:
            if not pm:
                un_matched_predictions = True
                break
        if un_matched_predictions:
           print >> out_results, "Unmatched Predictions"
           for el in range( 0, len(predict) ):
               if not predict_match[ el ]:
                   print >> out_results, "             %5.2f" % predict[ el ]

        print >> out_results, "-" * 80

print >> out_results, ""

cnt_match = len( all_dists )

print >> out_results, "\n Summary of results\n"
print >> out_results, "Number of matches:   %-i" % cnt_match

sum_all_dists = 0.0
sum_sq = 0.0
all_err = []
for a_dist in all_dists:
    sum_all_dists += a_dist
    sum_sq += a_dist * a_dist
    all_err.append( abs(a_dist) )

all_err.sort()

half_cnt = cnt_match / 2
if half_cnt * 2 < cnt_match: half_cnt += 1
median_err = all_err[ half_cnt ]

#print "sum_all_dists %e" % sum_all_dists
if cnt_match > 0:
    print >> out_results, "Average difference: %5.2f" % ( sum_all_dists / cnt_match )
    if cnt_match > 1:
        print >> out_results, "standard deviation: %5.2f" % math.sqrt( sum_sq / (cnt_match-1) )
        print >> out_results, "median err:         %5.2f" % median_err
