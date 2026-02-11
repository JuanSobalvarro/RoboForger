#define AppName "RoboForger"
#define AppVersion "2.1.0"
#define AppPublisher "JuSo"
#define AppExeName "RoboForger.exe"
#define BuildDir "./dist/main.dist"

[Setup]
; The app id is used so that windows can identify updates to the application when installing new versions
AppId={{0B48736C-9CCC-4923-8349-A985EB445ED5}
AppName={#AppName}
AppVersion={#AppVersion}
AppPublisher={#AppPublisher}

; install location default
DefaultDirName={autopf}\{#AppName}
DefaultGroupName={#AppName}

ArchitecturesInstallIn64BitMode=x64compatible
ArchitecturesAllowed=x64compatible

LicenseFile=./LICENSE

OutputDir=./installer
OutputBaseFilename=RoboForger_Setup_{#AppVersion}_x64
; lzma compression means smaller installer size
Compression=lzma
; solid compression means better compression ratio
SolidCompression=yes
WizardStyle=modern

SetupIconFile=./RoboForger/resources/icon.ico

[Languages]
Name: "english"; MessagesFile: "compiler:Default.isl"

[Tasks]
; Shows user the option to create a desktop icon
Name: "desktopicon"; Description: "{cm:CreateDesktopIcon}"; GroupDescription: "{cm:AdditionalIcons}"; Flags: unchecked

[Files]
; include exe
Source: "{#BuildDir}\{#AppExeName}"; DestDir: "{app}"; Flags: ignoreversion

; copy everything else
Source: "{#BuildDir}\*"; DestDir: "{app}"; Flags: ignoreversion recursesubdirs createallsubdirs

[Icons]
; icon index means which icon to use from the .ico file (0 is the first)
; Start Menu Icon
Name: "{group}\{#AppName}"; Filename: "{app}\{#AppExeName}"; IconFilename: "{app}\resources\icon.ico"; IconIndex: 0
; Desktop Icon only if the user selected the option
Name: "{userdesktop}\{#AppName}"; Filename: "{app}\{#AppExeName}"; Tasks: desktopicon; IconFilename: "{app}\resources\icon.ico"; IconIndex: 0

[Run]
; run the application after installation if the user selected the option
Filename: "{app}\{#AppExeName}"; Description: "{cm:LaunchProgram,{#AppName}}"; Flags: nowait postinstall skipifsilent