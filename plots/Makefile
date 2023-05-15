# dsm: There's a general incantation for this, but easier to just write it 
default: iso_scale_sweep-crop.pdf iso_security_sweep-crop.pdf

%-crop.pdf : %.pdf
	pdfcrop $< $@

clean:
	rm *-crop.pdf
