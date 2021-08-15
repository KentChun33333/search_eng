import nltk
import wget
import tarfile
import os 

nltk.download('stopwords')
model_url = "https://cloudstor.aarnet.edu.au/plus/s/hpfhUC72NnKDxXw/download"
outdir = "data/model"

if __name__ == "__main__":
    print(f"[doc2vec weight] download from: {model_url}")
    
    fname = wget.download(model_url, out=outdir)
        
    if fname.endswith("tar.gz") or fname.endswith("tgz"):
        tar = tarfile.open(fname, "r:gz")
        tar.extractall(outdir)
        tar.close()
    elif fname.endswith("tar"):
        tar = tarfile.open(fname, "r:")
        tar.extractall(outdir)
        tar.close()
    print(f"[doc2vec weight] unzipped {fname}")
        
    os.remove(fname)
    print(f"[doc2vec weight] Finished")
