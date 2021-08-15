import nltk
import wget
import tarfile
import os 

def extract(tar_url, extract_path='.'):
    tar = tarfile.open(tar_url, 'r')
    for item in tar:
        tar.extract(item, extract_path)
        if item.name.find(".tgz") != -1 or item.name.find(".tar") != -1:
            extract(item.name, "./" + item.name[:item.name.rfind('/')])


nltk.download('stopwords')
model_url = "https://cloudstor.aarnet.edu.au/plus/s/hpfhUC72NnKDxXw/download"
outdir = "data/model"


print(f"[doc2vec weight] download from: {model_url}")

fname = wget.download(model_url, out=outdir)

print(f"[doc2vec weight] saved at {fname}")

if fname.endswith("tar.gz") or fname.endswith("tgz"):
    tar = tarfile.open(fname, "r:gz")
    tar.extractall(outdir)
    tar.close()
elif fname.endswith("tar"):
    tar = tarfile.open(fname, "r:")
    tar.extractall(outdir)
    tar.close()
    
os.remove(fname)