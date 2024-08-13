PYTHON=python3
HEIGHT=10
WIDTH=10
DEBUG_LEVEL=1
FPS=25
FMEM=4
NBRSNAKES=05
RANDSEED=00000

GAME=mazer.py

# demo:
# 	$(eval DEBUG_LEVEL=2)

# 	$(eval HEIGHT=10)
# 	$(eval WIDTH=10)
# 	$(eval NBRSNAKES=09)
# 	$(eval RANDSEED=00000)

# 	$(eval FPS=25)
# # 	@for FMEM in 0 1 2 3 4 5 ; do 
# 	@for FMEM in 0 1 2 3 4 5 ; do \
# 		rm -f pics/mazer_*.png ; \
# 		$(PYTHON) ${GAME} --height ${HEIGHT} --width ${WIDTH} --debug_level ${DEBUG_LEVEL} --random_seed ${RANDSEED} --nbr_snakes ${NBRSNAKES} --fear_memory $$FMEM ; \
# 		bash ./pics/scale_mazes.sh ${HEIGHT} ${WIDTH} $$FMEM ${NBRSNAKES} ${RANDSEED}; \
# 		bash ./mpeg/make_movie.sh ${HEIGHT} ${WIDTH} $$FMEM ${NBRSNAKES} ${RANDSEED} ${FPS} mazer_${HEIGHT}x${WIDTH}_demo_fear_$$FMEM.mp4 ; \
# 	done

scan:
# 	rm -f ./pics/mazer_*.png
	@$(PYTHON) ${GAME} --parameter_scan 1 --height ${HEIGHT} --width ${WIDTH}
#	@bash ./pics/scale_mazes.sh ${HEIGHT} ${WIDTH} ${FMEM} ${NBRSNAKES} ${RANDSEED}
#	@if [ ${DEBUG_LEVEL} -gt 1 ]; then \
#		bash ./mpeg/make_movie.sh ${HEIGHT} ${WIDTH} ${FMEM} ${NBRSNAKES} ${RANDSEED} ${FPS} mazer_${HEIGHT}x${WIDTH}_f${FMEM}_s${NBRSNAKES}_r${RANDSEED}.mp4 ; \
#	fi


# %:
# # 	$(eval RANDSEED=0000${MAKECMDGOALS})
# 	$(eval RANDSEED=000${MAKECMDGOALS})
# 	rm -f ./pics/mazer_*.png
# 	@$(PYTHON) ${GAME} --height ${HEIGHT} --width ${WIDTH} --debug_level ${DEBUG_LEVEL} --random_seed ${RANDSEED} --nbr_snakes ${NBRSNAKES} --fear_memory $(FMEM)
# 	@bash ./pics/scale_mazes.sh ${HEIGHT} ${WIDTH} ${FMEM} ${NBRSNAKES} ${RANDSEED}
# 	@if [ ${DEBUG_LEVEL} -gt 1 ]; then \
# 		bash ./mpeg/make_movie.sh ${HEIGHT} ${WIDTH} ${FMEM} ${NBRSNAKES} ${RANDSEED} ${FPS} mazer_${HEIGHT}x${WIDTH}_f${FMEM}_s${NBRSNAKES}_r${RANDSEED}.mp4 ; \
# 	fi

# --------- even older Makefile code, just for reference: ---------

# demo:
# 	$(eval DEBUG_LEVEL=1)
# 	$(eval HEIGHT=10)
# 	$(eval WIDTH=10)
# 	$(eval NBRSNAKES=02)
# 	$(eval RANDSEED=00001)
# 	$(eval FPS=25)
# 	@for FMEM in 0 1 2 3 4 5 ; do \
# 		rm -f pics/mazer_${HEIGHT}x${WIDTH}_f$$FMEM_s${NBRSNAKES}_r${RANDSEED}_*.png ; \
# 		$(PYTHON) ${GAME} --height ${HEIGHT} --width ${WIDTH} --debug_level ${DEBUG_LEVEL} --random_seed ${RANDSEED} --fear_memory $$FMEM ; \
# 		bash ./pics/scale_mazes.sh ${HEIGHT} ${WIDTH} $$FMEM ${NBRSNAKES} ${RANDSEED}; \
# 		bash ./mpeg/make_movie.sh ${HEIGHT} ${WIDTH} $$FMEM ${NBRSNAKES} ${RANDSEED} ${FPS} mazer_${HEIGHT}x${WIDTH}_demo_fear_$$FMEM.mp4 ; \
# 	done

# 	$(eval DEBUG_LEVEL=1)
# 	$(eval WIDTH=10)
# 	$(eval HEIGHT=10)
# 	@for FMEM in 0 ; do \
# 		rm ./pics/mazer_${HEIGHT}x${WIDTH}_Mazer_f"$$FMEM"_*.png ; \
# 		$(PYTHON) mazer.py --height ${HEIGHT} --width ${WIDTH} --debug_level ${DEBUG_LEVEL} --fear_memory $$FMEM ; \
# 		bash ./pics/scale_mazes.sh ${HEIGHT} ${WIDTH} $$FMEM; \
# 		bash ./mpeg/make_movie.sh ${HEIGHT} ${WIDTH} ${FPS} $$FMEM ; \
# 	done

# run:
# 	bash ./mpeg/make_movie.sh ${HEIGHT} ${WIDTH} ${FPS} ${FMEM}

# run:
# 	@rm -f ./pics/mazer_${HEIGHT}x${WIDTH}_*.png
# 	@$(PYTHON) mazer.py --height ${HEIGHT} --width ${WIDTH} --debug_level ${DEBUG_LEVEL} --fear_memory ${FMEM}
# 	@bash ./pics/scale_mazes.sh ${HEIGHT} ${WIDTH} 
# 	@if [ ${DEBUG_LEVEL} -gt 0 ]; then \
# 		bash ./mpeg/make_movie.sh ${HEIGHT} ${WIDTH} ${FPS} $(MAKECMDGOALS) ; \
# 	fi

# %:
# 	rm -f ./pics/mazer_${HEIGHT}x${WIDTH}_f${FMEM}_*.png
# 	@$(PYTHON) ${GAME} --height ${HEIGHT} --width ${WIDTH} --debug_level ${DEBUG_LEVEL} --fear_memory $(MAKECMDGOALS)
# 	@bash ./pics/scale_mazes.sh ${HEIGHT} ${WIDTH} ${FMEM}
# 	@if [ ${DEBUG_LEVEL} -gt 0 ]; then \
# 		bash ./mpeg/make_movie.sh ${HEIGHT} ${WIDTH} ${FPS} $(MAKECMDGOALS) ; \
# 	fi


# %:
# 	rm -f ./pics/mazer_${HEIGHT}x${WIDTH}_f${FMEM}_s${NBRSNAKES}_r${RANDSEED}_*.png
# 	@$(PYTHON) ${GAME} --height ${HEIGHT} --width ${WIDTH} --debug_level ${DEBUG_LEVEL} --random_seed ${RANDSEED} --fear_memory $(FMEM)
# 	@bash ./pics/scale_mazes.sh ${HEIGHT} ${WIDTH} ${FMEM} ${NBRSNAKES} ${RANDSEED}
# 	@if [ ${DEBUG_LEVEL} -gt 0 ]; then \
# 		bash ./mpeg/make_movie.sh ${HEIGHT} ${WIDTH} ${FMEM} ${NBRSNAKES} ${RANDSEED} ${FPS} mazer_${HEIGHT}x${WIDTH}_f${FMEM}_s${NBRSNAKES}_r${RANDSEED}.mp4 ; \
# 	fi

# %:
# 	rm -f ./pics/mazer_${HEIGHT}x${WIDTH}_f${FMEM}_s${NBRSNAKES}_r${RANDSEED}_*.png
# 	@$(PYTHON) ${GAME} --height ${HEIGHT} --width ${WIDTH} --debug_level ${DEBUG_LEVEL} --random_seed ${RANDSEED} --fear_memory $(FMEM)
# 	@bash ./pics/scale_mazes.sh ${HEIGHT} ${WIDTH} ${FMEM} ${NBRSNAKES} ${RANDSEED}
# 	@if [ ${DEBUG_LEVEL} -gt 0 ]; then \
# 		bash ./mpeg/make_movie.sh ${HEIGHT} ${WIDTH} ${FMEM} ${NBRSNAKES} ${RANDSEED} ${FPS} mazer_${HEIGHT}x${WIDTH}_f${FMEM}_s${NBRSNAKES}_r${RANDSEED}.mp4 ; \
# 	fi
