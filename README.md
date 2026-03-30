# manim-projects
A directory for Manim Projects


## Example Commands
To render test scenes in low quality
```bash
manim --format gif -ql -o short test.py DifferentRotations
```


## WSL-Utilities Setup (For Windows on WSL)
Docs: https://wslu.wedotstud.io/wslu/

Install wslu for utilities access
```bash
sudo apt update
sudo apt install wslu
```

Tell Manim to use `wslview` instead of `xdg-open`
Add this environment variable to your shell config (`~/.bashrc` or `~/.zshrc`):

```bash
export BROWSER=wslview
```

Reload your shell:

```bash
source ~/.bashrc
```

Now when Manim finishes rendering, it will call:

```
wslview /path/to/video.mp4
```

…and Windows will open it in your default video player (Movies & TV, VLC, etc.).
