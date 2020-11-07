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

# replace the vocab handler in app.py
echo "app function return_vocab"
sed -n '/# FUNCTION return_vocab/q;p' $VP_HOME/vocprez/app.py > $VP_THEME_HOME/app_temp.py
cat $VP_THEME_HOME/app_return_vocab.py >> $VP_THEME_HOME/app_temp.py
sed -e '1,/# END FUNCTION return_vocab/ d' $VP_HOME/vocprez/app.py >> $VP_THEME_HOME/app_temp.py
mv $VP_THEME_HOME/app_temp.py $VP_HOME/vocprez/app.py

echo "customisation done"