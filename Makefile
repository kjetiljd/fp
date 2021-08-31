.PHONY: $(shell sed -n -e '/^$$/ { n ; /^[^ .\#][^ ]*:/ { s/:.*$$// ; p ; } ; }' $(MAKEFILE_LIST))

help:
	 @echo "$$(grep -hE '^\S+:.*##' $(MAKEFILE_LIST) | sed -e 's/:.*##\s*/:/' -e 's/^\(.\+\):\(.*\)/\\x1b[36m\1\\x1b[m:\2/' | column -c2 -t -s :)"

meta-update: ## Clone any repos that exist in your .meta file but aren't cloned locally
	@meta git update

pull: ## Run git pull --all --rebase --autostash on all repos
	@meta exec "git pull --all --rebase --autostash"

mainline: ## Switch all repos to mainline (main/master)
	@meta exec "git branch --all | sed 's/^[* ] //' | egrep '^main|^master' | xargs git checkout"

verify: ## Run mvn verify |./gradlew build on all
	cd fpsak-autotest/lokal-utvikling;./lokal-utvikling-fpsak.sh;cd ../..
	@meta exec "../script/verify.sh"

build: ## Run mvn clean install |./gradlew clean build
	@meta exec "../script/build.sh"
