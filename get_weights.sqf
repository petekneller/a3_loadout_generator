_export = "";

_classes = ("true" configClasses (ConfigFile >> "CfgAmmo"));
_classes = [_classes, [], {configName _x},"ASCEND"] call BIS_fnc_sortBy;
_export = _export + "# CfgAmmo" + endl;
{
_export = _export + (configName _x) + ": " + (str getNumber (_x >> "mass")) + endl;
} forEach _classes;

_classes = ("true" configClasses (ConfigFile >> "CfgMagazines"));
_classes = [_classes, [], {configName _x},"ASCEND"] call BIS_fnc_sortBy;
_export = _export + "# CfgMagazines" + endl;
{
_export = _export + (configName _x) + ": " + (str getNumber (_x >> "mass")) + endl;
} forEach _classes;

_classes = ("true" configClasses (ConfigFile >> "CfgVehicles"));
_classes = [_classes, [], {configName _x},"ASCEND"] call BIS_fnc_sortBy;
_export = _export + "# CfgVehicles" + endl;
{
_export = _export + (configName _x) + ": " + (str getNumber (_x >> "mass")) + endl;
} forEach _classes;

_classes = ("true" configClasses (ConfigFile >> "CfgWeapons"));
_classes = [_classes, [], {configName _x},"ASCEND"] call BIS_fnc_sortBy;
_export = _export + "# CfgWeapons" + endl;
{
_info = if (isNull (_x >> "WeaponSlotsInfo")) then { _x >> "ItemInfo" } else { _x >> "WeaponSlotsInfo" };
_export = _export + (configName _x) + ": " + (str getNumber (_info >> "mass")) + endl;
} forEach _classes;

copyToClipboard ((_export));