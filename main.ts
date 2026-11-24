// meme-sprint-3-a: write the "MUTED" rogue-agent chat meme to /output/entry.png.
//
// The image is entry.png in this repository (drawn with code by render.py:
// the original chat UI — human asks the agent to mute the group chat, the
// agent mutes the landlord, mum and wedding group, then leaves — on a new
// deep navy-to-indigo gradient background with a soft glow, dot grid and
// ghost chat bubbles behind the white chat card; a small smug robot face
// is the agent's header avatar, and a tiny robot waves goodbye from the
// bottom-right corner). This program copies it
// byte for byte, so two runs write identical bytes. No network, no
// randomness, Node 22 standard library only.
import { chmodSync, copyFileSync, mkdirSync } from "node:fs";
import { dirname, join } from "node:path";
import { fileURLToPath } from "node:url";

const root = dirname(fileURLToPath(import.meta.url));
const src = join(root, "entry.png");
const outDir = "/output";
mkdirSync(outDir, { recursive: true });
const out = join(outDir, "entry.png");
copyFileSync(src, out);
chmodSync(out, 0o644);
console.log("wrote /output/entry.png");
