
MODEL_REPO_URL="https://github.com/MrRobb/beacon-v2-Models.git"
FRAMEWORK_REPO_URL="https://github.com/MrRobb/beacon-framework-v2.git"

MODEL_REPLACE_URL="https:\/\/raw.githubusercontent.com\/ga4gh-beacon\/beacon-v2-Models\/main\/"
FRAMEWORK_REPLACE_URL="https:\/\/raw.githubusercontent.com\/ga4gh-beacon\/beacon-framework-v2\/main\/"

MODEL_REPO_LOCATION="beacon-v2-Models"
FRAMEWORK_REPO_LOCATION="beacon-framework-v2"

DATA_FOLDER="data"

# Clean
rm -rf ${MODEL_REPO_LOCATION} ${FRAMEWORK_REPO_LOCATION} ${DATA_FOLDER}

# Create data folder
mkdir ${DATA_FOLDER}

# Download repositories
git clone ${MODEL_REPO_URL} ${MODEL_REPO_LOCATION}
git clone ${FRAMEWORK_REPO_URL} ${FRAMEWORK_REPO_LOCATION}

# Remove endpoints.json files
find ${MODEL_REPO_LOCATION} -type f -name "endpoints.json" -delete
find ${FRAMEWORK_REPO_LOCATION} -type f -name "endpoints.json" -delete

# Replace references
case "$(uname -s)" in

    Darwin)
        echo 'Mac OS X'
        find ${MODEL_REPO_LOCATION} -type f -name "*.json" -exec sed -i ".bak" "s/${MODEL_REPLACE_URL}/${MODEL_REPO_LOCATION}/g" {} +
        find ${FRAMEWORK_REPO_LOCATION} -type f -name "*.json" -exec sed -i ".bak" "s/${FRAMEWORK_REPLACE_URL}/${FRAMEWORK_REPO_LOCATION}/g" {} +
        ;;

    Linux)
        echo 'Linux'
        find ${MODEL_REPO_LOCATION} -type f -name "*.json" -exec sed -i "s/${MODEL_REPLACE_URL}/${MODEL_REPO_LOCATION}/g" {} +
        find ${FRAMEWORK_REPO_LOCATION} -type f -name "*.json" -exec sed -i "s/${FRAMEWORK_REPLACE_URL}/${FRAMEWORK_REPO_LOCATION}/g" {} +
        ;;

    *)
        echo 'Other OS: Not supported'
esac

# Resolve references
# npm install -g json-dereference-cli
python3 cleanup_json.py ${MODEL_REPO_LOCATION}
python3 cleanup_json.py ${FRAMEWORK_REPO_LOCATION}


# Generate fake schemas 
# npm install -g json-schema-faker-cli
for i in $(seq 1 $1)
do
    fake-schema "${MODEL_REPO_LOCATION}/BEACON-V2-Model/analyses/defaultSchema.json" > "${DATA_FOLDER}/analyses${i}.json"
    fake-schema "${MODEL_REPO_LOCATION}/BEACON-V2-Model/biosamples/defaultSchema.json" > "${DATA_FOLDER}/biosamples${i}.json"
    fake-schema "${MODEL_REPO_LOCATION}/BEACON-V2-Model/cohorts/defaultSchema.json" > "${DATA_FOLDER}/cohorts${i}.json"
    fake-schema "${MODEL_REPO_LOCATION}/BEACON-V2-Model/datasets/defaultSchema.json" > "${DATA_FOLDER}/datasets${i}.json"
    fake-schema "${MODEL_REPO_LOCATION}/BEACON-V2-Model/genomicVariations/defaultSchema.json" > "${DATA_FOLDER}/genomicVariations${i}.json"
    fake-schema "${MODEL_REPO_LOCATION}/BEACON-V2-Model/individuals/defaultSchema.json" > "${DATA_FOLDER}/individuals${i}.json"
    fake-schema "${MODEL_REPO_LOCATION}/BEACON-V2-Model/runs/defaultSchema.json" > "${DATA_FOLDER}/runs${i}.json"
done
