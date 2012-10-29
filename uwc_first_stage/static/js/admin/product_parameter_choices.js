/*
 * Chosing paramets in case what project category now is select.
 */
django.jQuery(function(){
    var $ = django.jQuery;

    var productPage = function(options){
        this.options = options;
        this.productForm = {
            category: $('#id_category')
        };
        this.parameterFormSet = {
            parameter: $('select[name$=-parameter]'),
            value: $('select[name$=-value]')
        };

        var self = this;
        this.productForm.category.change(function(){
            self.onCategoryChange($(this));
        });

        this.parameterFormSet.parameter.live('change', function(){
            self.onParameterChange($(this));
        });

        self.onCategoryChange(this.productForm.category);
        self.onParameterChange(this.parameterFormSet.value);
    };

    productPage.prototype = {
        onCategoryChange: function(category){
            this._selectCorrectChoices(
                category,
                this.options.categoryParameters,
                this.parameterFormSet.parameter
            );
        },

        onParameterChange: function(parameter){
            this._selectCorrectChoices(
                parameter,
                this.options.parameterValues,
                this.parameterFormSet.value
            );

        },
        _selectCorrectChoices: function(el, choicesDict, field){
            var availableChoices = choicesDict[el.val()] || [],
                availableSelector = availableChoices.map(function(id){
                    return 'option[value=' + id +']';
                }).join(', ');
            // Hide all choices. Then show choices that belongs to current category/parameter.
            field.find('option').hide().filter(availableSelector).show();
        }
    };

    var options = getDjangoParam('adminProductPage');
    if(options){
        new productPage(options);
    }

});
