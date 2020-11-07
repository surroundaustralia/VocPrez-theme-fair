#echo "Styles"
#echo "copying $VP_THEME_HOME/style content to $VP_HOME/vocprez/view/style"
#cp $VP_THEME_HOME/style/* $VP_HOME/vocprez/view/style
#
#echo "Templates"
#echo "copying $VP_THEME_HOME/templates content to $VP_HOME/vocprez/view/templates"
#cp $VP_THEME_HOME/templates/* $VP_HOME/vocprez/view/templates

echo "Models"
echo "copying $VP_THEME_HOME/model content to $VP_HOME/vocprez/model"
cp $VP_THEME_HOME/model/* $VP_HOME/vocprez/model

echo "Config"
echo "creating VocPrez config with $VP_THEME_HOME/config.py"
echo "Alter config.py to include variables"
sed 's#$SPARQL_ENDPOINT#'"$SPARQL_ENDPOINT"'#' $VP_THEME_HOME/config.py > $VP_THEME_HOME/config_updated.py
mv $VP_THEME_HOME/config_updated.py $VP_HOME/vocprez/_config/__init__.py

echo "customisation done"