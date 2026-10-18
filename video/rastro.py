import cv2,numpy as np,sys,json
def ler(v):
    cap=cv2.VideoCapture(v);fr=[]
    while True:
        ok,f=cap.read()
        if not ok:break
        fr.append(f)
    return fr
def mascara(f):
    b,g,r=[f[:,:,k].astype(np.float32) for k in range(3)]
    mx=np.maximum(r,b);a=np.clip(1-(g-mx-12)/38,0,1);g2=np.minimum(g,mx+6)
    L=(r+g2+b)/3;sat=np.maximum(np.maximum(r,g2),b)-np.minimum(np.minimum(r,g2),b)
    return (np.clip((L-55)/30,0,1)*np.clip((40-sat)/14,0,1)*(a>=.5)),L*(a>=.5)
res={};prev=[]
for nome in ["jogador1","jogador2"]:
    fr=ler(f"video/{nome}.mp4");H,W=fr[0].shape[:2]
    w0,L0=mascara(fr[0]);wm=w0>.5
    y0=next(y for y in range(0,H,2) if wm[y,120:360:2].sum()>42)
    xs=[];ws=[]
    for y in range(y0+20,min(H,y0+90),4):
        idx=np.where(wm[y])[0]
        if len(idx)>10: xs.append((idx[0]+idx[-1])/2);ws.append(idx[-1]-idx[0])
    cx,sw=float(np.median(xs)),float(np.median(ws))
    # região do tronco no quadro 0 (sem mangas e sem a parte de baixo)
    tm=np.zeros((H,W),np.uint8);tm[int(y0):int(min(H-30,y0+sw*1.0)),int(cx-sw*.36):int(cx+sw*.36)]=1
    tm=(tm*(w0>.3)).astype(np.uint8)
    def a3(m):return np.vstack([m,[0,0,1]])
    def cinza(f):
        _,Li=mascara(f);return np.clip(Li,0,255).astype(np.uint8)
    g0=cinza(fr[0]);reg=cv2.dilate(tm,np.ones((9,9),np.uint8))
    P0=cv2.goodFeaturesToTrack(g0,400,0.005,5,mask=reg)
    Ms=[];M=np.eye(2,3,dtype=np.float32);gp=g0;pts=P0.copy();ref=P0.copy()
    for i,f in enumerate(fr):
        gi=cinza(f)
        if i>0:
            n1,st1,_=cv2.calcOpticalFlowPyrLK(gp,gi,pts,None,winSize=(21,21),maxLevel=3)
            n0,st0,_=cv2.calcOpticalFlowPyrLK(gi,gp,n1,None,winSize=(21,21),maxLevel=3)
            ok=(st1.ravel()==1)&(st0.ravel()==1)&(np.linalg.norm((n0-pts).reshape(-1,2),axis=1)<1)
            ref=ref[ok];pts=n1[ok]
            m,inl=cv2.estimateAffinePartial2D(ref,pts,method=cv2.RANSAC,ransacReprojThreshold=2)
            if m is not None:M=m.astype(np.float32)
            if len(pts)<150:
                # repõe pontos: acha novos no quadro atual e leva de volta ao quadro 0 pela transformação atual
                Mi=cv2.invertAffineTransform(M);rm=(cv2.warpAffine(tm,M,(W,H),flags=cv2.INTER_NEAREST))
                nv=cv2.goodFeaturesToTrack(gi,400,0.005,5,mask=cv2.dilate(rm,np.ones((9,9),np.uint8)))
                if nv is not None:
                    rv=(nv.reshape(-1,2)@Mi[:,:2].T+Mi[:,2]).reshape(-1,1,2).astype(np.float32)
                    pts=np.vstack([pts,nv]);ref=np.vstack([ref,rv])
            gp=gi
        Ms.append(M.copy())
    res[nome]={"cx":round(cx,1),"y0":int(y0),"sw":round(sw,1),"M":[[round(float(x),4) for x in m.flatten()] for m in Ms]}
    # prova visual: grade do quadro 0 levada para cada quadro
    row=[]
    for i in [0,40,80,120,160,191]:
        img=fr[i].copy();m=Ms[i]
        pts=np.array([[cx+sw*dx,y0+sw*dy] for dx in (-.3,0,.3) for dy in (.15,.33,.55,.8)],np.float32)
        q=pts@m[:,:2].T+m[:,2]
        for p in q:cv2.circle(img,(int(p[0]),int(p[1])),6,(0,0,255),-1)
        e=np.array([cx+sw*.19,y0+sw*.33]);e=m[:,:2]@e+m[:,2];cv2.circle(img,(int(e[0]),int(e[1])),int(sw*.09),(0,255,255),2)
        row.append(img)
    prev.append(np.hstack(row))
cv2.imwrite(sys.argv[1],cv2.resize(np.vstack(prev),None,fx=.42,fy=.42))
json.dump(res,open(sys.argv[2],"w"))
