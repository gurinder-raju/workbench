"""Offscreen preview renderer (moderngl) - polished gold, generic dial, strap.

python render.py            -> writes ../.renders/*.png (local only, git-ignored)
The dial artwork here is a generic placeholder for visualising proportions only.
"""
import math
import sys
from pathlib import Path

import moderngl
import numpy as np
import trimesh
from PIL import Image, ImageDraw

import params as P

HERE = Path(__file__).resolve().parent
TAG = P.TAG

VS = """
#version 330
uniform mat4 mvp;
in vec3 in_pos; in vec3 in_nrm;
out vec3 v_pos; out vec3 v_nrm;
void main(){ v_pos = in_pos; v_nrm = in_nrm; gl_Position = mvp * vec4(in_pos,1.0); }
"""
FS = """
#version 330
uniform vec3 view_dir;      // direction the camera looks (world)
uniform int mat;            // 0 gold, 1 dial, 2 strap, 3 dark (movement)
uniform sampler2D dial_tex;
uniform float dial_r;
in vec3 v_pos; in vec3 v_nrm;
out vec4 frag;
float sstep(float a,float b,float x){return smoothstep(a,b,x);}
vec3 env(vec3 r){
    // studio: bright overhead softbox, warm gradient, two side strips, a dark band
    float up = r.z;
    vec3 c = mix(vec3(0.42,0.40,0.37), vec3(0.95,0.93,0.90), sstep(-0.25,0.85,up));
    c = mix(c, vec3(0.80,0.78,0.74), sstep(-0.35,-0.85,up));        // white sweep below
    c += vec3(1.6) * sstep(0.80,0.93,up);                       // top softbox
    float side = abs(r.x);
    c += vec3(0.9) * sstep(0.75,0.9,side) * sstep(-0.3,0.2,up);  // side strips
    c *= 1.0 - 0.95 * (sstep(-0.16,-0.12,up) - sstep(-0.06,-0.02,up)); // thin black card
    return c;
}
void main(){
    vec3 n = normalize(v_nrm);
    vec3 V = -normalize(view_dir);
    if (dot(n,V) < 0.0) n = -n;
    if (mat == 0){
        vec3 F0 = vec3(1.00,0.80,0.42);
        vec3 R = reflect(-V, n);
        float c = clamp(dot(n,V),0.0,1.0);
        vec3 F = F0 + (1.0-F0)*pow(1.0-c,5.0);
        vec3 col = F * env(R) + 0.04*F0;
        col = col/(col+vec3(0.55)) * 1.45;                          // soft tonemap
        frag = vec4(pow(col, vec3(1.0/1.15)),1.0);
    } else if (mat == 1){
        vec2 uv = v_pos.xy / (2.0*dial_r) + 0.5;
        vec3 col = texture(dial_tex, vec2(uv.x, 1.0-uv.y)).rgb;
        float l = 0.80 + 0.20*clamp(dot(n, normalize(vec3(0.2,-0.3,1.0))),0.0,1.0);
        frag = vec4(col*l,1.0);
    } else if (mat == 2){
        vec3 L = normalize(vec3(0.3,-0.5,0.8));
        float d = 0.25 + 0.75*clamp(dot(n,L),0.0,1.0);
        vec3 H = normalize(L+V);
        float s = pow(clamp(dot(n,H),0.0,1.0), 18.0)*0.12;
        frag = vec4(vec3(0.045,0.043,0.045)*d*2.2 + s,1.0);
    } else if (mat == 4){
        vec3 R = reflect(-V, n);
        float c = clamp(dot(n,V),0.0,1.0);
        float F = 0.04 + 0.96*pow(1.0-c,5.0);
        vec3 col = env(R);
        frag = vec4(col, clamp(F*1.6,0.0,0.85));
    } else {
        frag = vec4(0.25,0.25,0.27,1.0);
    }
}
"""


def dial_texture(px=2048):
    s = px / (2 * P.R_DIAL)
    img = Image.new("RGB", (px, px), (246, 246, 243))
    d = ImageDraw.Draw(img)
    c = px / 2
    black = (25, 25, 25)
    # plain minute track
    r_out, r_in = 15.6, 14.9
    d.ellipse([c - r_out * s, c - r_out * s, c + r_out * s, c + r_out * s], outline=black, width=max(2, px // 700))
    for i in range(60):
        a = 2 * math.pi * i / 60
        r0 = 14.2 if i % 5 == 0 else r_in
        d.line([c + r0 * s * math.sin(a), c - r0 * s * math.cos(a),
                c + r_out * s * math.sin(a), c - r_out * s * math.cos(a)],
               fill=black, width=max(2, px // (300 if i % 5 == 0 else 900)))

    def hand(angle_deg, length, width, tail=0.0):
        a = math.radians(angle_deg)
        x1, y1 = c + length * s * math.sin(a), c - length * s * math.cos(a)
        x0, y0 = c - tail * s * math.sin(a), c + tail * s * math.cos(a)
        d.line([x0, y0, x1, y1], fill=black, width=int(width * s))

    # hands at 10:08:37
    hand(304, 8.5, 0.6)
    hand(48, 13.5, 0.45)
    hand(222, 14.5, 0.15, tail=3.0)
    d.ellipse([c - 0.7 * s, c - 0.7 * s, c + 0.7 * s, c + 0.7 * s], fill=black)
    return np.asarray(img)


def disc(r, z, n=256):
    a = np.linspace(0, 2 * np.pi, n, endpoint=False)
    v = np.c_[np.r_[0, r * np.cos(a)], np.r_[0, r * np.sin(a)], np.full(n + 1, z)]
    f = np.c_[np.zeros(n, int), 1 + np.arange(n), 1 + (np.arange(n) + 1) % n]
    return trimesh.Trimesh(v, f, process=False)


def strap_mesh(width=22.0, thick=2.4, z_mid=None, flat=16.0, bend_r=24.0, bend_deg=80, seg=60):
    z_mid = z_mid if z_mid is not None else P.Z_TUNNEL_FLOOR + thick / 2 + 0.15
    # centre-line in the YZ plane for +y half, mirrored for -y
    pts = [(y, z_mid) for y in np.linspace(0, flat, 12)]
    for t in np.linspace(0, math.radians(bend_deg), seg)[1:]:
        pts.append((flat + bend_r * math.sin(t), z_mid - bend_r * (1 - math.cos(t))))
    half = np.array(pts)
    path = np.r_[(half[::-1] * [-1, 1])[:-1], half]
    tang = np.gradient(path, axis=0)
    tang /= np.linalg.norm(tang, axis=1)[:, None]
    nrm = np.c_[-tang[:, 1], tang[:, 0]]       # in-plane normal (points "up")
    verts = []
    for (y, z), (ny, nz) in zip(path, nrm):
        for sx in (-width / 2, width / 2):
            for sn in (-thick / 2, thick / 2):
                verts.append((sx, y + sn * ny, z + sn * nz))
    verts = np.array(verts)
    faces = []
    n = len(path)
    for i in range(n - 1):
        a, b = 4 * i, 4 * (i + 1)
        # sides: bottom(0,2) top(3,1) left(1,0) right(2,3)
        for (p, q) in [(0, 2), (3, 1), (1, 0), (2, 3)]:
            faces.append((a + p, b + p, b + q))
            faces.append((a + p, b + q, a + q))
    return trimesh.Trimesh(verts, np.array(faces), process=False)


def smooth(m, angle=28):
    m = trimesh.graph.smooth_shade(m, angle=np.radians(angle))
    return m


_PROFILE = None


def analytic_normals(m):
    """Exact normals for vertices on the revolved pebble surface (render only)."""
    global _PROFILE
    from scipy.spatial import cKDTree
    from profile import fit, build
    if _PROFILE is None:
        s, r, z, phi, _ = build(fit())
        _PROFILE = (cKDTree(np.c_[r, z]), phi)
    tree, phi = _PROFILE
    v = m.vertices
    rv = np.hypot(v[:, 0], v[:, 1])
    d, i = tree.query(np.c_[rv, v[:, 2]])
    nrm = np.array(m.vertex_normals, copy=True)
    on = d < 0.004
    th = np.arctan2(v[:, 1], v[:, 0])
    sp, cp = np.sin(phi[i]), np.cos(phi[i])
    exact = np.c_[sp * np.cos(th), sp * np.sin(th), cp]
    # keep mesh normals where the surface is not the revolved profile (cut features)
    agree = np.einsum("ij,ij->i", exact, nrm) > 0.8
    nrm[on & agree] = exact[on & agree]
    return nrm


def look(az_deg, el_deg):
    """Camera direction for a camera placed at clock-angle az (deg from 12, clockwise)."""
    az, el = math.radians(az_deg), math.radians(el_deg)
    pos = np.array([math.sin(az) * math.cos(el), math.cos(az) * math.cos(el), math.sin(el)])
    return -pos


def mvp_ortho(view_dir, half_w, center, roll_up=(0, 0, 1)):
    f = np.asarray(view_dir, float); f /= np.linalg.norm(f)
    up = np.asarray(roll_up, float)
    if abs(np.dot(f, up)) > 0.99:
        up = np.array([0, 1, 0.0])
    r = np.cross(f, up); r /= np.linalg.norm(r)
    u = np.cross(r, f)
    M = np.eye(4)
    M[0, :3], M[1, :3], M[2, :3] = r, u, -f
    M[:3, 3] = -M[:3, :3] @ np.asarray(center, float)
    S = np.diag([1 / half_w, 1 / half_w, -1 / 80.0, 1])
    return S @ M


def render(scene, view_dir, out, size=1400, half_w=27.0, center=(0, 0, 6.5), bg=(18, 18, 20), ss=2):
    ctx = moderngl.create_standalone_context(require=330)
    prog = ctx.program(vertex_shader=VS, fragment_shader=FS)
    W = size * ss
    fbo = ctx.framebuffer(color_attachments=[ctx.texture((W, W), 4)],
                          depth_attachment=ctx.depth_texture((W, W)))
    fbo.use()
    ctx.enable(moderngl.DEPTH_TEST)
    ctx.clear(*(np.array(bg) / 255.0), 1.0)
    tex = ctx.texture((2048, 2048), 3, dial_texture().tobytes())
    tex.build_mipmaps()
    tex.use(0)
    prog["dial_tex"] = 0
    prog["dial_r"] = P.R_DIAL
    mvp = mvp_ortho(view_dir, half_w, center)
    prog["mvp"].write(mvp.T.astype("f4").tobytes())
    prog["view_dir"].value = tuple(np.asarray(view_dir, float) / np.linalg.norm(view_dir))
    opaque = [(m, k) for m, k in scene if k != 4]
    glass = [(m, k) for m, k in scene if k == 4]
    for i, (mesh, mat) in enumerate(opaque + glass):
        if mat == 4:
            ctx.enable(moderngl.BLEND)
            ctx.blend_func = moderngl.SRC_ALPHA, moderngl.ONE_MINUS_SRC_ALPHA
        v = mesh.vertices[mesh.faces].reshape(-1, 3).astype("f4")
        if mat == 0:
            vn = mesh.metadata.get("nrm")
            vn = mesh.vertex_normals if vn is None else vn
            nrm = vn[mesh.faces].reshape(-1, 3).astype("f4")
        else:
            nrm = np.repeat(mesh.face_normals, 3, axis=0).astype("f4")
        buf = ctx.buffer(np.hstack([v, nrm]).tobytes())
        vao = ctx.vertex_array(prog, [(buf, "3f 3f", "in_pos", "in_nrm")])
        prog["mat"] = mat
        vao.render(moderngl.TRIANGLES)
    img = Image.frombytes("RGBA", (W, W), fbo.read(components=4)).transpose(Image.FLIP_TOP_BOTTOM)
    img = img.convert("RGB").resize((size, size), Image.LANCZOS)
    img.save(out)
    ctx.release()
    return out


def load_scene(with_strap=True, with_dial=True, parts=("case_body", "caseback_bridge")):
    scene = []
    for name in parts:
        m = smooth(trimesh.load(P.STL_DIR / f"{TAG}_{name}.stl"))
        m.metadata["nrm"] = analytic_normals(m)
        scene.append((m, 0))
    crown = trimesh.load(P.STL_DIR / f"{TAG}_crown.stl")
    T = trimesh.transformations
    M = T.translation_matrix((0, P.SPOT_FACE_Y + P.CROWN_GAP, P.Z_STEM)) @ T.rotation_matrix(math.radians(-90), (1, 0, 0))
    crown.apply_transform(M)
    scene.append((smooth(crown, 20), 0))
    if with_dial:
        scene.append((disc(P.R_DIAL, P.Z_DIAL_TOP), 1))
        scene.append((disc(P.R_CRYSTAL, P.Z_CRYSTAL_TOP), 4))
        scene.append((disc(P.R_BORE, P.Z_FLOOR + 0.01), 3))
    if with_strap:
        scene.append((strap_mesh(), 2))
    return scene


VIEWS = {
    # name: (camera clock angle, elevation, half width, center)
    "front": (180, 90, 25.5, (0, 0.8, 6.5)),
    "side": (125, 22, 25.5, (0, 0, 5.5)),
    "profile_3oclock": (90, 0, 25.5, (0, 0, 6.5)),
    "profile_12oclock": (0, 0, 25.5, (0, 0, 6.5)),
    "three_quarter": (150, 38, 25.5, (0, 0, 5.0)),
    "back_three_quarter": (200, -50, 25.5, (0, 0, 4.0)),
    "crown_closeup": (35, 22, 7.0, (0, 21.5, 8.5)),
    "back_no_strap": (160, -55, 25.5, (0, 0, 4.0), False),
}

if __name__ == "__main__":
    outdir = P.PREVIEW_DIR
    outdir.mkdir(exist_ok=True)
    which = sys.argv[1:] or list(VIEWS)
    for name in which:
        az, el, hw, ctr = VIEWS[name][:4]
        strap = VIEWS[name][4] if len(VIEWS[name]) > 4 else True
        scene = load_scene(with_strap=strap)
        p = render(scene, look(az, el), outdir / f"{P.VERSION}_{name}.png", half_w=hw, center=ctr)
        print("wrote", p)
