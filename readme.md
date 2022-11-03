# Why getcbd?

When I am attempting the quiz provided by the original
[CBD](http://chemistrybydesign.oia.arizona.edu/) GUI, I find it a bit
unsatisfactory that I can only see one step at one time.

So, I homebrewed this little program to help people with similar needs.

Python 3, and its `requests` and `pillow` libraries, are required.

If you don't have these libraries, you can install them like:

```shell
pip install requests
pip install pillow
```

A web browser is necessary if you want to view the results.

## Set up / update metadata cache

Because the CBD's API transmits a huge load of data that evolves very slowly,
I recommend caching them.

First, run the following command to get the "list" of syntheses:

```shell
py getcbd.py -r
```

When asked for the full name of the synthesis, just pick a random one from the
list. Note that the "full name" includes the author and year in brackets.

If the command exited normally, you should see a file called `info_cache.json`
in the current working directory.

Then, invoke the following command, whose execution may be very lengthy:

```shell
py update_info.py
```

If the network unfortunately failed, you can reissue the command and choose `N`
when prompted whether to start from scratch.

## Viewing a specific synthesis

Run `getcbd.py` without the `-r` option allows the program to read the cache
instead of performing requests over the network.

When prompted, enter the full name of the synthesis.

The program will print out several status messages and then start downloading
the images. A checkpoint message is printed every 5 images so that you know
the program is still alive.

After the program exits, you can view the `result.html` with a browser.

The result web page will feature two exotically styled buttons, a link to the
paper and a scrollbar to zoom in or out on the synthesis.

By default, the site the link points to is `https://doi.org`. You can change
this by passing the `-s https://your.site.com` option to `getcbd.py`.

## Credits

First, I must convey my gratitude to the founders, developers and various
contributors to [Chemistry By Design](http://chemistrybydesign.oia.arizona.edu/).
It's their selfless work and the resulting database that made this work
possible.

Also to the team of ChOers at HEZ, who made many tough aesthetical decisions
for me and provided invaluable feedback on the user interface.

Good luck, and enjoy!
