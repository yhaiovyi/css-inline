import multiprocessing
from contextlib import suppress

import inlinestyler.utils
import premailer
import pynliner
import pytest
import toronado

import css_inline

SIMPLE_HTML = """<html>
<head>
    <title>Test</title>
    <style>
        h1, h2 { color:blue; }
        strong { text-decoration:none }
        p { font-size:2px }
        p.footer { font-size: 1px}
    </style>
</head>
<body>
    <h1>Big Text</h1>
    <p>
        <strong>Solid</strong>
    </p>
    <p class="footer">Foot notes</p>
</body>
</html>"""
SIMPLE_HTMLS = [SIMPLE_HTML] * 5000
MERGE_HTML = """<html>
<head>
    <title>Test</title>
    <style>
        h1, h2 { color:blue; }
        strong { text-decoration:none }
        p { font-size:2px }
        p.footer { font-size: 1px}
    </style>
</head>
<body>
    <h1 style="background-color: black;">Big Text</h1>
    <p style="background-color: black;">
        <strong style="background-color: black;">Solid</strong>
    </p>
    <p class="footer" style="background-color: black;">Foot notes</p>
</body>
</html>"""
MERGE_HTMLS = [MERGE_HTML] * 5000
REALISTIC_HTML = """<!DOCTYPE HTML PUBLIC "-//W3C//DTD HTML 4.01 Transitional//EN">
<html>
<head>
        <title> Newsletter</title>
    <meta name="viewport" content="width = 620" />
<style type="text/css">
img {margin:0}
a.bluelink:link,a.bluelink:visited,a.bluelink:active {color:#5b7ab3; text-decoration: none}
a.bluelink:hover {color:#5b7ab3; text-decoration: underline}
</style>
<style media="only screen and (max-device-width: 480px)" type="text/css">
* {line-height: normal !important; -webkit-text-size-adjust: 125%}
</style>
</head>

<body bgcolor="#FFFFFF" style="margin:0; padding:0">
<table width="100%" bgcolor="#FFFFFF" cellpadding="0" cellspacing="0" align="center" border="2">
    <tr>
        <td style="padding: 30px"><!--
--><table width="636" border="0" cellspacing="0" cellpadding="0" align="center">
    <tr>
        <td width="636"><img src="http://images.apple.com/data/retail/us/topcap.gif" border="0" alt="" width="636" height="62" style="display:block" /></td>
    </tr>
</table><!--
--><table width="636" border="1" cellspacing="0" cellpadding="0" align="center" bgcolor="#fffef6">
    <tr>
        <td width="59" valign="top" background="http://images.apple.com/data/retail/us/leftbg.gif"><img src="http://images.apple.com/data/retail/us/leftcap.gif" width="59" height="302" border="1" alt="" style="display:block" /></td>
        <td width="500" align="left" valign="top"><!--
--><table width="500" border="1" cellspacing="0" cellpadding="0">
    <tr>
        <td width="379" align="left" valign="top">
<div><img src="http://images.apple.com/data/retail/us/headline.gif" width="330" height="29" border="1" alt="Thanks for making a reservation." style="display:block" /></div>
        </td>
        <td width="21" align="right" valign="top">
<div><img src="http://images.apple.com/data/retail/us/applelogo.gif" width="21" height="25" border="1" alt="" style="display:block" /></div>
        </td>
    </tr>
</table><!--
--><table width="500" border="1" cellspacing="0" cellpadding="0">
    <tr>
        <td width="500" align="left" valign="top">
<div><img src="http://images.apple.com/data/retail/us/line.gif" width="500" height="36" border="0" alt="" style="display:block" /></div>
        </td>
    </tr>
</table><!--
--><table width="500" border="1" cellspacing="0" cellpadding="0">
    <tr>
        <td width="10" align="left" valign="top"></td>
        <td width="340" align="left" valign="top">


<div style="margin: 0; padding: 2px 10px 0 0; font-family: Lucida Grande, Arial, Helvetica, Geneva, Verdana, sans-serif; color: #000000 !important; font-size:12px; line-height: 16px">Dear peter,</div>
<div style="margin: 0; padding: 12px 10px 0 0; font-family: Lucida Grande, Arial, Helvetica, Geneva, Verdana, sans-serif; color: #000000 !important; font-size:12px; line-height: 16px">You are scheduled for a Genius Bar appointment.</div>
<div style="margin: 0; padding: 12px 10px 0 0; font-family: Lucida Grande, Arial, Helvetica, Geneva, Verdana, sans-serif; color: #000000 !important; font-size:12px; line-height: 16px">Topic: <b>iPhone</b></div>
<div style="margin: 0; padding: 12px 10px 0 0; font-family: Lucida Grande, Arial, Helvetica, Geneva, Verdana, sans-serif; color: #000000 !important; font-size:12px; line-height: 16px">Date: <b>Wednesday, Aug 26, 2009</b></div>
<div style="margin: 0; padding: 12px 10px 0 0; font-family: Lucida Grande, Arial, Helvetica, Geneva, Verdana, sans-serif; color: #000000 !important; font-size:12px; line-height: 16px">Time: <b>11:10AM</b></div>
<div style="margin: 0; padding: 12px 10px 0 0; font-family: Lucida Grande, Arial, Helvetica, Geneva, Verdana, sans-serif; color: #000000 !important; font-size:12px; line-height: 16px">Location: <b>Apple Store, Regent Street</b></div>
        </td>
        <td width="150" align="left" valign="top">
<div style="margin: 0; padding: 2px 0 0 0; font-family: Lucida Grande, Arial, Helvetica, Geneva, Verdana, sans-serif; color:#808285; font-size:11px; line-height: 13px">Apple Store,</div>
<div style="margin: 0; padding: 0 0 0 0; font-family: Lucida Grande, Arial, Helvetica, Geneva, Verdana, sans-serif; color:#808285; font-size:11px; line-height: 13px">Regent Street</div>
<div style="margin: 0; padding: 7px 0 0 0; font-family: Lucida Grande, Arial, Helvetica, Geneva, Verdana, sans-serif; color:#808285; font-size:11px; line-height: 13px"><a href="http://concierge.apple.com/WebObjects/RRSServices.woa/wa/ics?id=ewoJInByaW1hcnlLZXkiID0gewoJCSJyZXNlcnZhdGlvbklEIiA9ICI1ODEyMDI2NCI7Cgl9OwoJImVudGl0eU5hbWUiID0gIlJlc2VydmF0aW9uIjsKfQ%3D%3D" style="font-family: Lucida Grande, Arial, Helvetica, Geneva, Verdana, sans-serif; font-size:11px; color:#5b7ab3" class="bluelink">Add this to your calendar<img src="http://images.apple.com/data/retail/us/bluearrow.gif" width="8" height="8" border="0" alt="" style="display:inline; margin:0" /></a></div>
<div style="margin: 0; padding: 7px 0 0 0; font-family: Lucida Grande, Arial, Helvetica, Geneva, Verdana, sans-serif; color:#808285; font-size:11px; line-height: 13px">If you are no longer able to attend this session, please <a href="http://concierge.apple.com/WebObjects/Concierge.woa/wa/cancelReservation?r=ewoJInByaW1hcnlLZXkiID0gewoJCSJyZXNlcnZhdGlvbklEIiA9ICI1ODEyMDI2NCI7Cgl9OwoJImVudGl0eU5hbWUiID0gIlJlc2VydmF0aW9uIjsKfQ%3D%3D" style="font-family: Lucida Grande, Arial, Helvetica, Geneva, Verdana, sans-serif; font-size:11px; color:#5b7ab3" class="bluelink">cancel</a> or <a href="http://concierge.apple.com/WebObjects/Concierge.woa/wa/cancelReservation?r=ewoJInByaW1hcnlLZXkiID0gewoJCSJyZXNlcnZhdGlvbklEIiA9ICI1ODEyMDI2NCI7Cgl9OwoJImVudGl0eU5hbWUiID0gIlJlc2VydmF0aW9uIjsKfQ%3D%3D" style="font-family: Lucida Grande, Arial, Helvetica, Geneva, Verdana, sans-serif; font-size:11px; color:#5b7ab3" class="bluelink">reschedule</a> your reservation.</div>
<div style="margin: 0; padding: 7px 0 0 0; font-family: Lucida Grande, Arial, Helvetica, Geneva, Verdana, sans-serif; color:#808285; font-size:11px; line-height: 13px"><a href="http://www.apple.com/retail/../uk/retail/regentstreet/map" style="font-family: Lucida Grande, Arial, Helvetica, Geneva, Verdana, sans-serif; font-size:11px; color:#5b7ab3" class="bluelink">Get directions to the store<img src="http://images.apple.com/data/retail/us/bluearrow.gif" width="8" height="8" border="0" alt="" style="display:inline; margin:0" /></a></div>
        </td>
    </tr>
</table><!--
--><table width="500" border="1" cellspacing="0" cellpadding="0">
    <tr>
    <td width="10"></td>
                <td width="490" align="left" valign="top">
                <br>
<div style="margin: 0; padding: 0 20px 0 0; font-family: Lucida Grande, Arial, Helvetica, Geneva, Verdana, sans-serif; color: #000000 !important; font-size:12px; line-height: 16px">We look forward to seeing you.</div>
<div style="margin: 0; padding: 0 20px 0 0; font-family: Lucida Grande, Arial, Helvetica, Geneva, Verdana, sans-serif; color: #000000 !important; font-size:12px; line-height: 16px">Your Apple Store team,</div>
<div style="margin: 0; padding: 0 20px 0 0; font-family: Lucida Grande, Arial, Helvetica, Geneva, Verdana, sans-serif; color: #000000 !important; font-size:12px; line-height: 16px">Regent Street</div>
        </td>
    </tr>
</table><!--
        --></td>
        <td width="59" valign="top" background="http://images.apple.com/data/retail/us/rightbg.gif"><img src="http://images.apple.com/data/retail/us/rightcap.gif" width="77" height="302" border="0" alt="" style="display:block" /></td>
    </tr>
</table><!--
--><table width="636" border="1" cellspacing="0" cellpadding="0" align="center">
    <tr>
        <td width="636"><img src="http://images.apple.com/data/retail/us/bottomcap.gif" border="0" alt="" width="636" height="62" style="display:block" /></td>
    </tr>
</table><!--
BEGIN FOOTER
--><table width="498" border="1" cellspacing="0" cellpadding="0" align="center">
    <tr>
        <td style="padding-top:22px">
<div style="font-family: Geneva, Verdana, Arial, Helvetica, sans-serif; font-size:9px; line-height: 12px; color:#b4b4b4">TM and copyright &copy; 2008 Apple Inc. 1 Infinite Loop, MS 303-3DM, Cupertino, CA 95014.</div>
<div style="font-family: Geneva, Verdana, Arial, Helvetica, sans-serif; font-size:9px; line-height: 12px; color:#b4b4b4"><a href="http://www.apple.com/legal/" style="font-family: Geneva, Verdana, Arial, Helvetica, sans-serif; font-size:9px;line-height: 12px; color:#b4b4b4; text-decoration:underline">All Rights Reserved</a> / <a href="http://www.apple.com/enews/subscribe/"  style="font-family: Geneva, Verdana, Arial, Helvetica, sans-serif; font-size:9px; line-height: 12px;color:#b4b4b4; text-decoration:underline">Keep Informed</a> / <a href="http://www.apple.com/legal/privacy/" style="font-family: Geneva, Verdana, Arial, Helvetica, sans-serif; font-size:9px; line-height: 12px; color:#b4b4b4; text-decoration:underline">Privacy Policy</a> / <a href="https://myinfo.apple.com/cgi-bin/WebObjects/MyInfo/" style="font-family: Geneva, Verdana, Arial, Helvetica, sans-serif; font-size:9px; line-height: 12px; color:#b4b4b4; text-decoration:underline">My Info</a></div>
        </td>
    </tr>
</table><!--
        --></td>
    </tr>
</table>
</body>
</html>"""
REALISTIC_HTMLS = [REALISTIC_HTML] * 100


def parametrize_functions(
    *funcs, ids=("css_inline", "premailer", "pynliner", "inlinestyler", "toronado")
):
    return pytest.mark.parametrize("func", funcs, ids=ids)


all_functions = parametrize_functions(
    css_inline.inline,
    premailer.transform,
    pynliner.fromString,
    inlinestyler.utils.inline_css,
    toronado.from_string,
)


def parallel(func):
    return lambda data: multiprocessing.Pool().map(func, data)


all_many_functions = parametrize_functions(
    css_inline.inline_many,
    parallel(css_inline.inline),
    parallel(premailer.transform),
    parallel(pynliner.fromString),
    parallel(inlinestyler.utils.inline_css),
    parallel(toronado.from_string),
    ids=(
        "css_inline",
        "css_inline_pyprocess",
        "premailer",
        "pynliner",
        "inlinestyler",
        "toronado",
    ),
)


@all_functions
@pytest.mark.benchmark(group="simple")
def test_simple(benchmark, func):
    benchmark(func, SIMPLE_HTML)


@all_many_functions
@pytest.mark.benchmark(group="simple many")
def test_simple_many(benchmark, func):
    benchmark(func, SIMPLE_HTMLS)


@all_functions
@pytest.mark.benchmark(group="merge")
def test_merge(benchmark, func):
    benchmark(func, MERGE_HTML)


@all_many_functions
@pytest.mark.benchmark(group="merge many")
def test_merge_many(benchmark, func):
    benchmark(func, MERGE_HTMLS)


@all_functions
@pytest.mark.benchmark(group="realistic")
def test_realistic(benchmark, func):
    benchmark(func, REALISTIC_HTML)


@all_many_functions
@pytest.mark.benchmark(group="realistic many")
def test_realistic_many(benchmark, func):
    benchmark(func, REALISTIC_HTMLS)


@pytest.mark.benchmark(group="exception")
def test_exception(benchmark):
    def func():
        with suppress(ValueError):
            css_inline.inline("", base_url="!wrong!")

    benchmark(func)
