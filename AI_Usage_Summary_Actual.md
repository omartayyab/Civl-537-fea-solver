# AI Usage Summary
---
## Tools Used
I used Gemini both as a Chrome search engine and LLM giuding me. I Did not use a built in like copilot or Claude to help me generate code directly in my editor. I definitely needed help understanding the lil_matrix csr_matrix` and when to use each among other things. See below.,

## What Was AI-Assisted vs. Written By Me

I wrote `compute_area`, `compute_B` ,`compute_D`, and `compute_K `. As these were the first few functions I wrote, I needed a lot of help familiarizing myself with the syntax. So If I didnt know how to define an array in Python, I would write as I would in Matlab and sometimes it will work. SOmetimes I would have to modify. I found it really interesting that the syntax is so similar. Using VScode to write in python was strange too as I first learned python on its own IDE v 2.7 I believe and it needed semi colons. Now it seems to be just fine. Even how to add a comment I had to ask Gemini and how to comment out a block of code. 


`assemble_R_parabolic_shear` I wrote this mostly, Including the Gauss point usage, computing the load vetor.. I needed some help parsing the last row and indexing up.

For `assemble_K`, I wrote the loop structure myself but GEmini again helped me the lil_matrix and CSR matrix.  I verified this was correct by printing the DOF indices for one element and checking by hand. I actually simplified parts of the code by preparing the Dofs vector correspond to each node.`assemble_R_uniform_tension` I wrote this initially but Gemini completed this.

The `generate_rect_mesh` was fun implement. It was ditto the same syntax. Meshgrid, linspace. Gemini introduced the Flatten() commands that saved a bit of headache. And reading the docstring I encountered a new DATASTRUCTURE called dictionary. I had to spend time understanding what it did. It was quite fun and closest thing to this I saw was in embedded system programming where we had register addresses and values inside each register bit. Gemini helped me get that set up and pass along with the correct syntax and "protocol"?! . 

`generate_plate_with_hole_mesh` I knew I neeeded to do a polar coordinate transform. Until i realized that the mEsh I generated was only radial.. I needed to chat with GEmini to get this right. It was very clever and simple.. But it made some issues. Odd angular mesh instances worked great. BUt the even ones were chopping off the corner triangle. I spent alot of time nodal numerating, Counting nodes etc. AI was suggesting hacks, I didnt like that, so I opened up APP.py and with some review I was able to add the first practical constraint. Basically if you look at the angular slider, it only allows an odd number.. Lol.

Connectivity matrix bit was pretty intuitive at this point. Due to my troubles earlier I was already swapping diagonals around to define triangles. but I would say it was a joint effort especially because we had to ensure that we identified all the edges correctly and pass the boundary tags accurately.  The fall back MESH was not an option. 

Almost similar story in Post processing. However, here a new function was added to add an extra functionality. 


## One Case Where AI Was Wrong

Not sure where it was wrong. It was being AI. It would adopt hacky tactics. It will give nonsensical conclusions. I remember encountering them when I was varying the Geometry, I wish I had made notes. But I think 100% of the issues with App.py were coded by Gemini but proposed by me. Whereas it GEMINI proposed a Hack of some sort... 

## What I Learned

So much, Docker, Python, VScode, Streamlit. And FEA ofcourse. THis is one of the most projects I have done and One I will continue to work on,

Future versions may include:

1) Identifying boundary nodes directly on the UI and define them through a drop down,
2) Support for more element types. So, LST, Bilinear, Quad, Axisymmetric elements.
3) Add the spherical void in an infinite solid. 
4) Add deformed mesh overlay to undeformed Mesh. 
5) Complex boundary conditions and loading conditions, Function driven.
