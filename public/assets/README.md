Place your photo directories here and run build, it will generate a gallery for you.  
Or you can run python script `tool/import_albums.py` to import albums.  
`pnpm run import-albums` will do the same thing.  
The directory structure should be like this:
```
import-albums
├── album1
│   ├── photo1.jpg
│   ├── photo2.jpg
│   └── ...
├── album2
├── ...
└── ...
```
If it is a new album, you need to fill the album information in `src/utils/meta.json`  
DO NOT directly place photos in `src/public/assets/albums/`