_dic = {
    # 已有的文件类型映射关系
    "unknown": "default",
    "folder": "folder",
    "txt": "file_txt",
    "pdf": "file_pdf",
    "jpg": "file_img",
    "jpeg": "file_img",
    "png": "file_img",
    "gif": "file_img",
    "doc": "file_word",
    "docx": "file_word",
    "xls": "file_excel",
    "xlsx": "file_excel",
    "ppt": "file_ppt",
    "pptx": "file_ppt",
    "mp3": "file_music",
    "wav": "file_music",
    "mp4": "file_video",
    "avi": "file_video",
    "html": "file_html",
    "bt": "file_bt",
    "cad": "file_cad",
    "cloud": "file_cloud",
    "code": "file_code",
    "exe": "file_exe",
    "flash": "file_flash",
    "iso": "file_iso",
    "psd": "file_psd",
    "zip": "file_zip",
    # 补充的文件类型映射关系
    "py": "file_code",  # Python代码文件
    "java": "file_code",  # Java代码文件
    "c": "file_code",  # C语言代码文件
    "cpp": "file_code",  # C++代码文件
    "cs": "file_code",  # C#代码文件
    "php": "file_code",  # PHP代码文件
    "js": "file_code",  # JavaScript代码文件
    "css": "file_code",  # CSS文件
    "xml": "file_code",  # XML文件
    "json": "file_code",  # JSON文件
    "yaml": "file_code",  # YAML文件
    "md": "file_code",  # Markdown文件
    "sql": "file_code",  # SQL文件
    "rb": "file_code",  # Ruby代码文件
    "swift": "file_code",  # Swift代码文件
    "vb": "file_code",  # Visual Basic代码文件
    "perl": "file_code",  # Perl代码文件
    "lua": "file_code",  # Lua代码文件
    "sh": "file_code",  # Shell脚本文件
    "bat": "file_code",  # 批处理文件
    "ps1": "file_code",  # PowerShell脚本文件
    "coffee": "file_code",  # CoffeeScript代码文件
    "ts": "file_code",  # TypeScript代码文件
    "r": "file_code",  # R代码文件
    "h": "file_code",  # 头文件
    "hpp": "file_code",  # C++头文件
    "hxx": "file_code",  # C++头文件
    "hh": "file_code",  # C++头文件
    "m": "file_code",  # Objective-C代码文件
    "mm": "file_code",  # Objective-C++代码文件
    "go": "file_code",  # Go代码文件
    "kt": "file_code",  # Kotlin代码文件
    "dart": "file_code",  # Dart代码文件
    "scala": "file_code",  # Scala代码文件
    "rust": "file_code",  # Rust代码文件
    "ejs": "file_code",  # EJS文件
    "jade": "file_code",  # Jade文件
    "less": "file_code",  # Less文件
    "sass": "file_code",  # Sass文件
    "scss": "file_code",  # SCSS文件
    "stylus": "file_code",  # Stylus文件
    "tsx": "file_code",  # TypeScript React文件
    "vue": "file_code",  # Vue文件
    "yml": "file_code",  # YAML文件
    "csv": "file_excel",  # CSV文件
    "xlsb": "file_excel",  # Excel二进制文件
    "ods": "file_excel",  # OpenDocument电子表格文件
    "numbers": "file_excel",  # Numbers文件
    "key": "file_ppt",  # Keynote文件
    "pps": "file_ppt",  # PowerPoint幻灯片
    "odp": "file_ppt",  # OpenDocument演示文稿文件
    "sldx": "file_ppt",  # PowerPoint Open XML幻灯片文件
    "ai": "file_ai",  # Adobe Illustrator文件
    "eps": "file_ai",  # Encapsulated PostScript文件
    "svg": "file_ai",  # 可缩放矢量图形文件
    "torrent": "file_bt",  # Torrent文件
    "dwg": "file_cad",  # AutoCAD DWG文件
    "dxf": "file_cad",  # AutoCAD DXF文件
    "rvt": "file_cad",  # Revit文件
    "skp": "file_cad",  # SketchUp文件
    "sldprt": "file_cad",  # SolidWorks零件文件
    "sldasm": "file_cad",  # SolidWorks装配文件
    "f3d": "file_cad",  # Fusion 360设计文件
    "step": "file_cad",  # STEP文件
    "stl": "file_cad",  # STL文件
    "igs": "file_cad",  # IGS文件
    "x_t": "file_cad",  # Parasolid文本文件
    "x_b": "file_cad",  # Parasolid二进制文件
    "dwf": "file_cad",  # Design Web Format文件
    "ifc": "file_cad",  # Industry Foundation Classes文件
    "bim": "file_cad",  # Building Information Modeling文件
    "rfa": "file_cad",  # Revit家族文件
    "rft": "file_cad",  # Revit模板文件
    "rte": "file_cad",  # Revit模板文件
    "gcode": "file_cad",  # G代码文件
    "asm": "file_cad",  # SolidWorks组件文件
    "prt": "file_cad",  # SolidWorks零件文件
    "drw": "file_cad",  # SolidWorks图纸文件
    "edrw": "file_cad",  # eDrawings文件
    "eprt": "file_cad",  # eDrawings零件文件
    "easm": "file_cad",  # eDrawings装配文件
    "pcf": "file_cad",  # Piping数据交换文件
    "sketch": "file_cad",  # Sketch文件
    "sat": "file_cad",  # ACIS模型文件
    "3dm": "file_cad",  # Rhino 3D模型文件
    "x3d": "file_cad",  # X3D文件
    "blend": "file_cad",  # Blender文件
    "fbx": "file_cad",  # Autodesk FBX文件
    "max": "file_cad",  # 3ds Max文件
    "ma": "file_cad",  # Maya ASCII文件
    "mb": "file_cad",  # Maya二进制文件
    "obj": "file_cad",  # OBJ文件
    "lxo": "file_cad",  # Luxology Modo文件
    "lwo": "file_cad",  # LightWave 3D对象文件
    "daz": "file_cad",  # DAZ Studio文件
    "ifczip": "file_cad",  # IFC压缩文件
    "vwx": "file_cad",  # Vectorworks文件
    "asmx": "file_cad",  # Solid Edge组件文件
    "parx": "file_cad",  # Solid Edge零件文件
    "dftx": "file_cad",  # Solid Edge绘图文件
    "car": "file_cad",  # CAR文件
    "sklib": "file_cad",  # SketchUp库文件
    "wire": "file_cad",  # Wire文件
    "bip": "file_cad",  # Lumion场景文件
    "f3z": "file_cad",  # ZBrush项目文件
    "ztl": "file_cad",  # ZBrush工具文件
    "zpr": "file_cad",  # ZBrush项目文件
    "scad": "file_cad",  # OpenSCAD脚本文件
    "sla": "file_cad",  # Slic3r配置文件
    "factory": "file_cad",  # PrusaSlicer配置文件
    "mcf": "file_cad",  # Medusa CAD文件
    "oxc": "file_cad",  # OXygen CAD文件
    "brd": "file_cad",  # PCB布局文件
    "dcm": "file_cad",  # Discreet可视化文件
    "dgn": "file_cad",  # MicroStation设计文件
    "dmt": "file_cad",  # DELFTship模型文件
    "draft": "file_cad",  # FreeCAD绘图文件
    "xd": "file_cad",  # Adobe XD文件
    "storyboard": "file_cad",  # Storyboard文件
    "aep": "file_cad",  # Adobe After Effects项目文件
    "moho": "file_cad",  # Moho动画文件
    "fla": "file_cad",  # Adobe Animate文件
    "cpt": "file_cad",  # CorelDRAW模板文件
    "cdr": "file_cad",  # CorelDRAW文件
    "cdx": "file_cad",  # CorelDRAW压缩文件
    "cmx": "file_cad",  # CorelDRAW交换文件
    "cpr": "file_cad",  # Corel PHOTO-PAINT RAW文件
    "cpx": "file_cad",  # Corel PHOTO-PAINT压缩文件
    "csl": "file_cad",  # Corel SCRIPT文件
    "des": "file_cad",  # Corel DESIGNER文件
    "ds4": "file_cad",  # DAZ Studio 4场景文件
    "dazip": "file_cad",  # DAZ Install Manager安装包
    "mmod": "file_cad",  # MikuMikuDance模型文件
    "pmx": "file_cad",  # MikuMikuDance模型文件
    "x": "file_cad",  # DirectX模型文件
    "upk": "file_cad",  # Unreal Engine Package文件
    "c4d": "file_cad",  # Cinema 4D文件
    "lxp": "file_cad",  # Luxology Modo产品文件
    "lxt": "file_cad",  # Luxology Modo绘图文件
    "mtl": "file_cad",  # MTL文件
    "ogex": "file_cad",  # Open Game Engine Exchange文件
    "rh": "file_cad",  # Rhino 3D模型文件
    "cga": "file_cad",  # ESRI CityEngine CGA文件
    "otx": "file_cad",  # OpenType文件
    "w3x": "file_cad",  # Warcraft III地图文件
    "wmo": "file_cad",  # World of Warcraft物体文件
    "blp": "file_cad",  # Blizzard纹理文件
    "mpq": "file_cad",  # Blizzard MPQ存档文件
    "flt": "file_cad",  # OpenFlight文件
    "m3": "file_cad",  # StarCraft II模型文件
    "m3u": "file_music",  # M3U播放列表文件
    "pls": "file_music",  # PLS播放列表文件
    "asx": "file_music",  # Windows Media播放列表文件
    "wpl": "file_music",  # Windows Media播放列表文件
    "cue": "file_music",  # CUE音乐信息文件
    "log": "file_code",  # 日志文件
    "sub": "file_video",  # 字幕文件
    "srt": "file_video",  # SubRip字幕文件
    "ass": "file_video",  # Advanced SubStation Alpha字幕文件
    "vtt": "file_video",  # WebVTT字幕文件
    "idx": "file_video",  # VobSub索引文件
    "sup": "file_video",  # DVD格式字幕文件
    "sbv": "file_video",  # YouTube字幕文件
    "conf": "file_code",  # 配置文件
    "cfg": "file_code",  # 配置文件
    "ini": "file_code",  # INI配置文件
    "toml": "file_code",  # TOML配置文件
    "properties": "file_code",  # Properties文件
    "reg": "file_code",  # Windows注册表文件
    "cmd": "file_code",  # Windows命令文件
    "bash": "file_code",  # Bash脚本文件
    "zsh": "file_code",  # Zsh脚本文件
    "ksh": "file_code",  # KornShell脚本文件
    "tcsh": "file_code",  # TENEX C Shell脚本文件
    "csh": "file_code",  # C Shell脚本文件
    "awk": "file_code",  # AWK脚本文件
    "pl": "file_code",  # Perl脚本文件
    "jsp": "file_code",  # Java Server Pages文件
    "asp": "file_code",  # Active Server Pages文件
    "aspx": "file_code",  # ASP.NET文件
    "cshtml": "file_code",  # Razor页面文件
    "xhtml": "file_code",  # XHTML文件
    "mkd": "file_code",  # Markdown文件
    "markdown": "file_code",  # Markdown文件
    "pug": "file_code",  # Pug文件
    "haml": "file_code",  # HAML文件
    "hbs": "file_code",  # Handlebars文件
    "mustache": "file_code",  # Mustache文件
    "rtf": "file_txt",  # 富文本格式文件
    "odt": "file_word",  # OpenDocument文本文件
    "ott": "file_word",  # OpenDocument文本模板文件
    "dot": "file_word",  # Word模板文件
    "dotx": "file_word",  # Word Open XML模板文件
    "ppsx": "file_ppt",  # PowerPoint Open XML幻灯片文件
    "pot": "file_ppt",  # PowerPoint模板文件
    "potx": "file_ppt",  # PowerPoint Open XML模板文件
    "xlt": "file_excel",  # Excel模板文件
    "xltx": "file_excel",  # Excel Open XML模板文件
    "odg": "file_img",  # OpenDocument绘图文件
    "odc": "file_excel",  # OpenDocument图表文件
    "odb": "file_excel",  # OpenDocument数据库文件
    "wpd": "file_word",  # WordPerfect文档
    "htm": "file_html",  # HTML文件
    "bmp": "default",  # BMP图像文件
    "tiff": "file_img",  # TIFF图像文件
    "indd": "file_psd",  # Adobe InDesign文档文件
    "stp": "file_cad",  # STEP文件
    "rar": "file_zip",  # 压缩文件
    "7z": "file_zip",  # 压缩文件
    "tar": "file_zip",  # 压缩文件
    "gz": "file_zip",  # 压缩文件
    "bz2": "file_zip",  # 压缩文件
    "xz": "file_zip",  # 压缩文件
    "dll": "file_exe",  # 动态链接库文件
    "com": "file_exe",  # DOS命令文件
    "jar": "file_exe",  # Java存档文件
    "apk": "file_exe",  # Android安装包文件
    "deb": "file_exe",  # Debian软件包文件
    "rpm": "file_exe",  # RPM软件包文件
    "app": "file_exe",  # macOS应用程序文件
    "dmg": "file_exe",  # macOS磁盘映像文件
    "tar.gz": "file_zip",  # 压缩文件
    "tar.bz2": "file_zip",  # 压缩文件
    "tar.xz": "file_zip",  # 压缩文件
    "tar.z": "file_zip",  # 压缩文件
    "tar.lz": "file_zip",  # 压缩文件
    "tar.lzma": "file_zip",  # 压缩文件
    "war": "file_exe",  # Java Web存档文件
    "ear": "file_exe",  # Java Enterprise存档文件
    "epub": "file_pdf",  # EPUB电子书文件
    "mobi": "file_pdf",  # Mobipocket电子书文件
    "azw": "file_pdf",  # Amazon Kindle电子书文件
    "azw3": "file_pdf",  # Amazon Kindle电子书文件
    "djvu": "file_pdf",  # DjVu文件
    "xps": "file_pdf",  # XML Paper Specification文件
    "cbz": "file_pdf",  # Comic Book Archive文件
    "cbr": "file_pdf",  # Comic Book Archive文件
    "cb7": "file_pdf",  # Comic Book Archive文件
    "cba": "file_pdf",  # Comic Book Archive文件
    "cbt": "file_pdf",  # Comic Book Archive文件
    "lz": "file_zip",  # 压缩文件
    "lzma": "file_zip",  # 压缩文件
    "lzo": "file_zip",  # 压缩文件
    "lzip": "file_zip"
}
