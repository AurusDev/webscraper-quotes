[Setup]
AppId={{A6D9AB7B-9F4B-4C5D-8E70-AURUS-WEBSCRAPER}}
AppName=Webscraper Quotes
AppVersion=1.0.0
AppPublisher=AurusDev
DefaultDirName={pf}\Webscraper Quotes
DefaultGroupName=Webscraper Quotes
OutputBaseFilename=WebscraperQuotesInstaller
Compression=lzma
SolidCompression=yes
ArchitecturesInstallIn64BitMode=x64
DisableProgramGroupPage=no
SetupIconFile=build\icon.ico
UninstallDisplayIcon={app}\WebscraperQuotes_v1.exe

[Languages]
Name: "portuguese"; MessagesFile: "compiler:Languages\Portuguese.isl"

[Tasks]
Name: "desktopicon"; Description: "Criar atalho na Área de Trabalho"; GroupDescription: "Opções adicionais:"; Flags: unchecked

[Files]
Source: "build\WebscraperQuotes_v1.exe"; DestDir: "{app}"; Flags: ignoreversion
Source: "build\icon.ico"; DestDir: "{app}"; Flags: ignoreversion

[Icons]
Name: "{group}\Webscraper Quotes"; Filename: "{app}\WebscraperQuotes_v1.exe"; IconFilename: "{app}\icon.ico"
Name: "{userdesktop}\Webscraper Quotes"; Filename: "{app}\WebscraperQuotes_v1.exe"; IconFilename: "{app}\icon.ico"; Tasks: desktopicon

[Run]
Filename: "{app}\WebscraperQuotes_v1.exe"; Description: "Executar Webscraper Quotes agora"; Flags: nowait postinstall skipifsilent
