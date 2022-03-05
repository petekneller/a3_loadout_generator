yq -y 'with_entries(select(.value != 0))' <from_get_weights.sqf>.yaml | sort
