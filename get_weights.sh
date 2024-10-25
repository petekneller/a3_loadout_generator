yq -y 'to_entries | sort_by(.key) | from_entries' <from_get_weights.sqf>.yaml 

# or to merge
yq -sy 'map(to_entries) | flatten | group_by(.key) | map(reduce .[] as $i ({}; $i * .)) | from_entries' weights.yaml <from_get_weights.sqf>.yaml > <output_file>.yaml