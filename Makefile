default: help

##@ Utility
help:  ## Display this help
	@awk 'BEGIN {FS = ":.*##"; printf "\nUsage:\n  make \033[36m\033[0m\n"} /^[a-zA-Z_-]+:.*?##/ { printf "  \033[36m%-15s\033[0m %s\n", $$1, $$2 } /^##@/ { printf "\n\033[1m%s\033[0m\n", substr($$0, 5) } ' $(MAKEFILE_LIST)


btsetup: ## Spin up a single node bitable instance an populate
	@gcloud bigtable instances create talkinbaseball --display-name=talkinbaseball --cluster-storage-type=HDD --cluster-config=id=talkinbaseball-c1,zone=us-west1-c,nodes=1
	@gcloud bigtable instances tables create profiles --instance talkinbaseball --project mague-tf --column-families=p --no-deletion-protection
	@cbt -project=mague-tf -instance=talkinbaseball set profiles shoheiohtani p:Notes="Shohei is from the Tohoku region of Japan, where the best players come from" p:PlayerId="660271"
	@cbt -project=mague-tf -instance=talkinbaseball set profiles loganwebb p:Notes="Webb lathers and rinses, but never repeats and certainly never smiles while doing so" p:PlayerId="657277"
	@cbt -project=mague-tf -instance=talkinbaseball set profiles mookiebetts p:Notes="Mookie's chain caused the earth's axis to move by 0.1 degrees" p:PlayerId="605141"
	@cbt -project=mague-tf -instance=talkinbaseball set profiles mannymachado p:Notes="Machado is famous for the crying meme" p:PlayerId="592518"
	@gcloud bigtable materialized-views create fun_notes --instance=talkinbaseball  --query 'SELECT _key AS id, p["Notes"] AS notes, p["PlayerId"] AS player_id FROM profiles ORDER BY id, notes, player_id'

btdelete: ## Shutdown the Spanner instance
	@gcloud spanner instances delete useridentity

