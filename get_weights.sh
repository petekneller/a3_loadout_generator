yq -y 'to_entries | sort_by(.key) | from_entries' <from_get_weights.sqf>.yaml 

# or to merge
yq -sy 'map(to_entries) | flatten | unique_by(.key) | sort_by(.key) | from_entries' weights.yaml <from_get_weights.sqf>.yaml