{ player removeItem _x } forEach (uniformItems player);
for "_i" from 1 to 1000 do { player addItemToUniform "ACE_banana"; };
{ player removeItem _x } forEach (vestItems player);
for "_i" from 1 to 1000 do { player addItemToVest "ACE_banana"; };
{ player removeItem _x } forEach (backpackItems player);
for "_i" from 1 to 1000 do { player addItemToBackpack "ACE_banana"; };