#!/usr/bin/python3

import face_recognition as fr
import os, argparse
import pandas as pd
from PIL import Image
from tqdm import tqdm

def html_parse(file,path_output):

	with open("main.html","w") as f:

		html = """<style>.team_member {
				  width:100%;
				  position:relative;
				  overflow:hidden;
				  height:250px;
				}

				.info {
				  height:100%;
				}

				.info img {
				  width:100%;
				  transition: all .4s ease-out .1s;
				   -moz-transition: all .4s ease-out .1s;
				   -webkit-transition: all .4s ease-out .1s;
				}

				.info h5 {
				  padding: 10px 10px 0 0;
				  margin: 0 0 10px 3px;
				  line-height: 1em;
				  opacity: 1;
				  transition: all .2s ease-out .1s;
				   -moz-transition: all .2s ease-out .1s;
				   -webkit-transition: all .2s ease-out .1s;
				  font-size: 1.125em;
				}

				.info h6 {
				  padding:0 10px 0 0;
				  font-size:12px;
				  margin:0 0 0 3px;
				  line-height:1em;
				  text-transform:uppercase;
				  color:#999;
				  opacity:1;
				  transition: all .2s ease-out .1s;
				   -moz-transition: all .2s ease-out .1s;
				   -webkit-transition: all .2s ease-out .1s;
				}

				.info_reveal {
				  height:100%; 
				  transition: all .3s ease-in 0s;
				   -moz-transition: all .3s ease-in 0s;
				   -webkit-transition: all .23s ease-in 0s;
				  position:absolute;
				  width:100%;
				  left:0;
				  top:-100%;
				  background: #915BD9;
				}

				.info_reveal h6 {
				  padding: 20px 8px 5px 8px;
				  line-height: 1.1em;
				    margin-bottom: 20px;
				    color: #fff;
				  font-size: 1em;
				}

				.info_reveal p {
				  padding:0 8px;
				  font-size:15px;
				  line-height: 1.2em;
				  color: #073a2e;
				  font-weight:400;  
				}

				.info_reveal a {
				  color: #073a2e;
				    word-break: break-word;
				  text-decoration:none;
				}

				.info_reveal a:hover {
				  color: #073a2e;
				}


				.responsive_grid {
				 display:block;
				 margin:0;
				 padding:0;
				 list-style:none;
				}

				.responsive_grid li {
				 cursor:pointer;
				 width: 16.66667%;
				 padding: 0 10px 10px;
				 display:block;
				 height:auto;
				 float:left;
				 margin-bottom:10px;
				}

				.responsive_grid li:hover .info_reveal,
				.responsive_grid li:focus .info_reveal{
				 left: 0;
				 top:0;
				 transition: all .3s ease-out .1s;
				   -moz-transition: all .3s ease-out .1s;
				   -webkit-transition: all .3s ease-out .1s;
				}

				.responsive_grid li:hover .info img,
				.responsive_grid li:focus .info img {
				  width:210%;
				  margin-left:-50%;
				  transition: all .4s ease-in 0s;
				   -moz-transition: all .4s ease-in 0s;
				   -webkit-transition: all .4s ease-in 0s;
				}

				.responsive_grid li:hover .info h5,
				.responsive_grid li:focus .info h5,
				.responsive_grid li:hover .info h6,
				.responsive_grid li:focus .info h6 {
				  opacity: 0;
				  transition: opacity .2s linear 0s;
				   -moz-transition: opacity .2s linear 0s;
				   -webkit-transition: opacity .2s linear 0s;
				}
				body {
				  font-family: "HelveticaNeue-Light", "Helvetica Neue Light", "Helvetica Neue", Helvetica, Arial, "Lucida Grande", sans-serif;
				  padding: 50px 100px;
				  max-width: 55.25em;
				  font-family: 'Open Sans', sans-serif;
				}

				h5, h6, .info_reveal a {
				  font-family: 'Open Sans Condensed', sans-serif;
				}</style>

				<link href='https://fonts.googleapis.com/css?family=Open+Sans|Open+Sans+Condensed:700&subset=latin,latin-ext' rel='stylesheet' type='text/css'>
				<ul class="responsive_grid">"""

		banner = """  <li>
	    <div class="team_member">
	       <div class="info">
	         <img src="{0}{1}{2}" alt=""/>
	         <h5>{3}</h5>
	         <h6>Parcours : {4}</h6> 
	      </div>
	      <div class="info_reveal">
	        <h6><br/>Parcours : {4}</h6>
	        <p><a href="mailto:{5}">{5}</a></p>
	        <p>{6}</p>
	      </div>
	    </div>
	  </li>"""

		data = list(read_csv(file))

		f.write(html)
		f.write("\n")
		for i in range(len(data)):
			f.write(banner.format(path_output,
								str(i)+"_"+data[i][0].replace(" ","_")+"_"+data[i][1].replace(" ","_")+".",	
								os.listdir(path_output)[i].split(".")[-1],										data[i][0]+" "+data[i][1],	
								data[i][2],	
								data[i][3],	
								data[i][4]))
			f.write("\n")
		f.write("</ul>")

def read_csv(file):
	data = pd.read_csv(file)
	return zip(data["nom"],data["prenom"],data["filiere"],data["email"],data["numero"])

def read_csv_names(file):
	data = pd.read_csv(file)
	return zip(data["nom"],data["prenom"])

def newsize(size,dim):
	w,h = dim
	ratio = w/h
	if w>=h:
		new_size = (int(ratio*size[1]),size[1])
	else:
		new_size = (size[0],int(1/ratio*size[0]))
	return new_size

def facial_recognition(new_size,dim,file,i):
	w,h = dim
	print(w,h)
	print(fr.load_image_file(file))
	print(i,fr.face_locations(fr.load_image_file(file)))
	top,right,bottom,left = [int(i*(new_size[0]/w)) for i in fr.face_locations(fr.load_image_file(file))[0]]
	return left,top,right,bottom

def crop_width(localisations,new_size,size):

	left,top,right,bottom = localisations

	diff = (size[0]-(right-left))/2
	left,top,right,bottom = left-diff,0,right+diff,new_size[1]
	if left<0:
		top=-1*left+top	
		left = 0
	elif right>new_size[0]:
		left=left-(right-new_size[0])
		right = new_size[0]

	return (left,top,right,bottom)

def crop_height(localisations,new_size,size):

	left,top,right,bottom = localisations

	diff = (size[1]-(bottom-top))/2
	left,top,right,bottom = 0,top-diff,new_size[0],bottom+diff
	if top<0:
		bottom=-1*top+bottom
		top = 0
	elif bottom>new_size[1]:
		top=top-(bottom-new_size[1])
		bottom = new_size[1]

	return (left,top,right,bottom)

def main(path_input="data/",path_output="done/",size=(250,300),csv="cpes.csv"):

	files = [path_input+f for f in os.listdir(path_input)]

	tosave = [path_output+str(f)+"_"+"_".join(list(read_csv_names(csv))[f]).replace(" ","_")+"."+os.listdir(path_input)[f].split(".")[-1] for f in range(len(os.listdir(path_input)))]

	print("Chargement en cours :)")
	for i in tqdm(range(len(files))):

		im = Image.open(files[i])
		w,h = im.size 
		new_size = newsize(size, im.size)
		im = im.resize(new_size)

		localisations = facial_recognition(new_size, (w,h), files[i],i)

		if w>=h:
			im = im.crop(crop_width(localisations,new_size,size))
		else:
			im = im.crop(crop_height(localisations,new_size,size))

		im.save(tosave[i])

	html_parse(csv,path_output)


if __name__ == "__main__":

	parser = argparse.ArgumentParser()

	parser.add_argument("-i", "--input",help="Fichier CSV d'input",default="cpes.csv")
	parser.add_argument("-p","--path",help="Dossier contenant les photographies", default="data/")
	parser.add_argument("-w","--width",type=int,help="Largeur maximale de chaque photographie",default=250)
	parser.add_argument("-l","--height",type=int,help="Hauteur maximale de chaque photographie",default=300)
	parser.add_argument("-o","--output",help="Dossier de sortie des fichiers traités",default="done/")

	args = parser.parse_args()
	main(args.path,args.output,(args.width,args.height),args.input)