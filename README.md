# Modular Music Visualizer

An attempt to make a free (as in freedom) and open source music visualization tool for the music production community

## Small showcase

![Demo image of MMV](repo/demo-2.jpg)

[Link to unlisted video of the full music in the image above](https://youtu.be/UXncwltx-pQ)

(it's an work in progress track I'm producing)

_The DAW is Ardour 6.0_

*Bonus!!*

[Unlisted video of old version of MMV](https://youtu.be/BhpLwaR1Oj8)

# Huge reorganization of core code is being worked on, expect instability

# Idea

So I am a Free and Open Source music producer hobbyist that also happens to be a code hobbyist and at some point it's inevitable I'd be releasing my tracks to the internet and create some project to make the world a better place.

The problem is, I don't want to release a video of the track on a platform with a static image or just recording the screen nor pay for some software to generate an "music visualization" for me without much control of it.

So I searched up for a free (as in freedom and price) tool that does exactly that, they do exist but aren't as good as they could be, most of the time a bit basic..

Then I just got into this opportunity on making a suckless (as in quality not minimalism I see you lol) music visualization tool with the programming languages and tools I love and care.

# Table of contents

   * [Running](#running)
      * [Linux](#linux)
      * [Windows](#windows)
   * [Goals, what is being developed](#goals-what-is-being-developed)
   * [Contributing](#contributing)


# Wiki is TODO

Lot's of stuff are moving on the code and being rewritten, when things are more stable I'll write a proper guide.

Use the example scripts located on the project root folder as for now for learning and / or read the code, it's pretty well commented

# Running

Please, if you are running this project from source, after installing the Python dependencies install [pillow-simd](https://github.com/uploadcare/pillow-simd) instead of vanilla Pillow, preferably with the AVX2 instructions explained in its repo if your CPU supports so.

As you can see [here](https://python-pillow.org/pillow-perf/), `pillow-simd` is faster by a lot on imaging processing, although most stuff is done with skia, rotation is still done with PIL.

#### IMPORTANT!!

If you're going to venture out on creating your own MMV scripts, I higly recommend reading the basics of Python [here](https://learnxinyminutes.com/docs/python/), it doesn't take much to read and will avoid some beginner pitfals.

Though you probably should be fine by just creating a copy of the example scripting I provide on the repo and reading through my comments and seeing the Python code working, it's pretty straightforward as I tried to simplify the syntax and naming functions with a more _"concrete"_ meaning. 

## Linux

Install Python and git on your distribution

- Arch / Arch based (Manjaro): `sudo pacman -Syu python git`

- Ubuntu / Debian based: `sudo apt install python git`

Open a shell on desired dir to clone the repo

`git clone https://github.com/Tremeschin/modular-music-visualizer`

`cd modular-music-visualizer`

[Use a Python venv](https://github.com/Tremeschin/dandere2x-tremx/wiki/Python-venvs) (recommended):

- `python -m venv mmv-venv`

- `source ./mmv-venv/bin/activate`

`pip install -r mmv/requirements.txt`

You can run a example file under `mmv/example*.py` with `python mmv/example*.py` (you should know how to do it right?)

I include a few free assets under the `mmv/assets/free_assets` folder, you can use them at your disposal, they were generated with my other project called [PyGradienter](https://github.com/Tremeschin/pygradienter) that I'm merging the two here in MMV :)

There's also the example of calling pygradienter from a MMV script

## Windows

TODO, need testing

# Goals, what is being developed

#### High priority / now

- [x] (basically 90% done) Huge refactor of the code and moving a lot of stuff, simplifying interpolation and making Modifier classes individually

- [x] ~~(stuck) R&D alternative methods for converting SVG --> PNG under Python because Windows (or could someone write a small guide for installing cairo under Windows that works? I didn't put much effort until now on this)~~ `skia-python` solved all this

- [x] ~~(half worked) R&D alternative methods for rendering the final frame (each branch is one way I tried _- and failed or wasn't really efficient_)~~ `skia-python` seems VERY promising, `pyvips` almost worked but skia was faster

#### Medium priority

- [x] ~~Profile the code, find bottlenecks, general optimization on most expensive functions~~ Video background is a bottleneck now because moving textures back and forth from the GPU, other than that the code is running fast

- [ ] (boring) Update requirements.txt

- [x] ~~Make a proper presentation / demo / gif about MMV and link on README~~ didn't work well

#### Ideas for the future or waiting to be executed

- [ ] Progression bar (square, circle, pie graph?)

- [ ] Rectangle bars visualizer (only circle + linear or symetric currently)

- [ ] Rain images on pygradienter and rain particle generator?

# Contributing

Please read [CONTRIBUTING.md](docs/CONTRIBUTING.md) file :)
