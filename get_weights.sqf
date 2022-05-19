_export = "";

_classes = ("true" configClasses (ConfigFile >> "CfgAmmo"));
_classes = [_classes, [], {configName _x},"ASCEND"] call BIS_fnc_sortBy;
{
	if (!isNull (_x >> "mass")) then {
		_export = _export + (configName _x) + ":" + endl;
		_export = _export + "  mass: " + (str getNumber (_x >> "mass")) + endl;
	};
} forEach _classes;

_classes = ("true" configClasses (ConfigFile >> "CfgMagazines"));
_classes = [_classes, [], {configName _x},"ASCEND"] call BIS_fnc_sortBy;
{
	if (!isNull (_x >> "mass")) then {
		_export = _export + (configName _x) + ":" + endl;
		_export = _export + "  mass: " + (str getNumber (_x >> "mass")) + endl;
		_export = _export + "  magazine: true" + endl;
	};
} forEach _classes;

_classes = ("true" configClasses (ConfigFile >> "CfgVehicles"));
_classes = [_classes, [], {configName _x},"ASCEND"] call BIS_fnc_sortBy;
{
	if (!isNull (_x >> "mass")) then {
		_export = _export + (configName _x) + ":" + endl;
		_export = _export + "  mass: " + (str getNumber (_x >> "mass")) + endl;
	};
} forEach _classes;

_classes = ("true" configClasses (ConfigFile >> "CfgWeapons"));
_classes = [_classes, [], {configName _x},"ASCEND"] call BIS_fnc_sortBy;
{
	_info = if (isNull (_x >> "WeaponSlotsInfo")) then { _x >> "ItemInfo" } else { _x >> "WeaponSlotsInfo" };
	if (!isNull (_info >> "mass")) then {
		_export = _export + (configName _x) + ":" + endl;
		_export = _export + "  mass: " + (str getNumber (_info >> "mass")) + endl;
	};
} forEach _classes;

copyToClipboard ((_export));