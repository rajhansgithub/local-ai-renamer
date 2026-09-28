; Inno Setup Script for Local Auto Image Renamer
; Produces AutoImageRenamer_Setup.exe

#define MyAppName "Local AI Renamer"
#define MyAppVersion "1.0.0"
#define MyAppPublisher "rajhansgithub"
#define MyAppExeName "LocalAIRenamer.exe"

[Setup]
AppId={{D37E6F52-8B91-4921-998E-7B930268481A}
AppName={#MyAppName}
AppVersion={#MyAppVersion}
AppPublisher={#MyAppPublisher}
DefaultDirName={autopf}\{#MyAppName}
DefaultGroupName={#MyAppName}
DisableProgramGroupPage=yes
PrivilegesRequired=lowest
OutputDir=installer_output
OutputBaseFilename=LocalAIRenamer_Setup
Compression=lzma2/ultra
SolidCompression=yes
WizardStyle=modern

[Languages]
Name: "english"; MessagesFile: "compiler:Default.isl"

[Tasks]
Name: "desktopicon"; Description: "{cm:CreateDesktopIcon}"; GroupDescription: "{cm:AdditionalIcons}"; Flags: unchecked
Name: "contextmenu"; Description: "Add 'Rename with Local AI' to Windows Explorer right-click context menu"; GroupDescription: "Explorer Integration:"; Flags: checkablechecked

[Files]
Source: "dist\LocalAIRenamer\*"; DestDir: "{app}"; Flags: ignoreversion recursesubdirs createallsubdirs; Check: DirExists(ExpandConstant('{src}\dist\LocalAIRenamer'))
Source: "dist\AutoImageRenamer\*"; DestDir: "{app}"; Flags: ignoreversion recursesubdirs createallsubdirs; Check: DirExists(ExpandConstant('{src}\dist\AutoImageRenamer'))
Source: "config.json"; DestDir: "{app}"; Flags: ignoreversion

[Icons]
Name: "{group}\{#MyAppName}"; Filename: "{app}\{#MyAppExeName}"
Name: "{group}\{cm:UninstallProgram,{#MyAppName}}"; Filename: "{uninstallexe}"
Name: "{autodesktop}\{#MyAppName}"; Filename: "{app}\{#MyAppExeName}"; Tasks: desktopicon

[Registry]
; Context Menu on Directory (Folder)
Root: HKCU; Subkey: "Software\Classes\Directory\shell\LocalAIRenamer"; ValueType: string; ValueData: "Rename with Local AI"; Flags: uninsdeletekey; Tasks: contextmenu
Root: HKCU; Subkey: "Software\Classes\Directory\shell\LocalAIRenamer"; ValueType: string; ValueName: "Icon"; ValueData: "{app}\{#MyAppExeName}"; Tasks: contextmenu
Root: HKCU; Subkey: "Software\Classes\Directory\shell\LocalAIRenamer\command"; ValueType: string; ValueData: """{app}\{#MyAppExeName}"" ""%1"""; Tasks: contextmenu

; Context Menu on Directory Background (Inside Folder)
Root: HKCU; Subkey: "Software\Classes\Directory\Background\shell\LocalAIRenamer"; ValueType: string; ValueData: "Rename with Local AI"; Flags: uninsdeletekey; Tasks: contextmenu
Root: HKCU; Subkey: "Software\Classes\Directory\Background\shell\LocalAIRenamer"; ValueType: string; ValueName: "Icon"; ValueData: "{app}\{#MyAppExeName}"; Tasks: contextmenu
Root: HKCU; Subkey: "Software\Classes\Directory\Background\shell\LocalAIRenamer\command"; ValueType: string; ValueData: """{app}\{#MyAppExeName}"" ""%V"""; Tasks: contextmenu

[Run]
Filename: "{app}\{#MyAppExeName}"; Description: "{cm:LaunchProgram,{#StringChange(MyAppName, '&', '&&')}}"; Flags: nowait postinstall skipifsilent
